import datetime
import os
import re
from subprocess import PIPE, Popen
from typing import Callable, Optional

from infiniguard_api.common import const
from infiniguard_api.lib.iguard_api_exceptions import IguardApiException
from infiniguard_api.lib.logging import iguard_logging

from infiniguard_api.lib.hw.output_parser import parse_async
from infiniguard_api.lib.hw.tasks import (task_start,
                                          task_end,
                                          get_task,
                                          task_update_files,
                                          task_update_line)
from infiniguard_api.lib.hw.threads import submit_task
import selectors

log = iguard_logging.get_logger(__name__)

USER_ROLES_TRANSLATE = {'backupuser': 'backupuser',
                        'airuser': 'airuser', 'workgroup': 'user'}

FILES_PER_INSERT = 5000  # How many files to insert in the database in each transaction
STDOUT = 1
STDERR = 2


def create_user_command(username, role, password, description=None):
    cmd_role = USER_ROLES_TRANSLATE[role]
    components = ['add', cmd_role]
    data = dict()
    if role == 'airuser':
        data['username'] = username
    else:
        data['name'] = username

    data['password'] = password

    if description is not None:
        data['desc'] = description

    components.append(data)

    return components


# /opt/DXi/syscli --edit backupuser --name 'test2' --password 'zzz' --desc 'New desc'
def update_user_command(username, role, password=None, description=None, admin=None):
    cmd_role = USER_ROLES_TRANSLATE[role]
    components = ['edit', cmd_role]
    data = dict()
    if role == 'airuser':
        data['username'] = username
    else:
        data['name'] = username

    if password is not None:
        data['password'] = password

    if description is not None:
        data['desc'] = description

    if admin is not None:
        data['admin'] = admin

    components.append(data)

    return components


# /opt/DXi/syscli --list backupuser
def list_users_command(role):
    cmd_role = USER_ROLES_TRANSLATE[role]
    components = ['list']
    components.extend([cmd_role])

    return components


# /opt/DXi/syscli --del backupuser --name test


def delete_user_command(username, role):
    cmd_role = USER_ROLES_TRANSLATE[role]
    components = ['del', cmd_role]
    data = dict()
    if role == 'airuser':
        data['username'] = username
    else:
        data['name'] = username

    components.append(data)

    return components


def execute_command(command):
    try:
        p = Popen(command,
                  shell=False,
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE,
                  close_fds=False)
        stdout, stderr = p.communicate()
        rc = p.returncode
    except OSError as e:
        log.error(repr(e))
        stdout = ''
        stderr = e.strerror
        rc = e.errno
    except Exception as e:
        log.error(repr(e))
        stdout = ''
        stderr = 'Failed'
        rc = 1
    if isinstance(stderr, bytes):
        stderr = stderr.decode("utf-8")
    if isinstance(stdout, bytes):
        stdout = stdout.decode("utf-8")
    return rc, stdout, stderr


def execute_command_sync(command, task_id):
    command = ['stdbuf', '-oL'] + command

    with Popen(command, stdout=PIPE, stderr=PIPE, shell=False, text=True) as p, \
            selectors.DefaultSelector() as sel:

        sel.register(p.stdout, selectors.EVENT_READ)
        sel.register(p.stderr, selectors.EVENT_READ)

        while True:
            for key, _ in sel.select():
                data = key.fileobj.readline()
                if not data:
                    sel.unregister(key.fileobj)
                    if not sel.get_map():
                        return p.wait()
                else:
                    fd = STDOUT if key.fileobj is p.stdout else STDERR
                    task_update_line(task_id, data.rstrip(), fd)

    return p.returncode


def _cmd_(command, obj, is_threaded=False, thread_id=None):
    log.info('{} {} {}'.format(command, obj, is_threaded))
    if is_threaded:
        task, err = get_task(thread_id)
        if not task:
            log.error(err)
            raise IguardApiException('Task not found')
        else:
            task_id = task[0].task_id
            task_start = task[0].start
            try:
                rc = execute_command_sync(command, task_id)
            except Exception:
                log.exception('Could not execute command')
                rc = 1
            stdout = ''
            stderr = ''
            task_end(task_id, task_start, rc, stdout, stderr)
    else:
        rc, stdout, stderr = execute_command(command)
        return rc, stdout, stderr


def _python_cmd_(cmd, args, thread_id=None):
    task_name = cmd.__name__
    task, err = get_task(thread_id)
    if not task:
        log.error(err)
        raise IguardApiException('Task not found')
    task = task[0]
    task_id = task.task_id
    task_start = task.start
    rc = -1
    stdout = ''
    stderr = 'Failed'
    try:
        if task_name == 'do_list_share':
            filelist = list()
            size = 0
            rc = 0
            stdout = ""
            stderr = ""
            for line in cmd(args):
                rc, stdout, stderr = line
                filelist.append(stdout)
                size += 1
                if size == FILES_PER_INSERT:
                    task_update_files(task_id, filelist)
                    filelist = list()
                    size = 0
            task_update_files(task_id, filelist)
            stdout = "Finished"
        elif task_name in ['do_ping', 'do_traceroute', 'do_mtu', 'do_dig']:
            for line, stdstream in cmd(args):
                task_update_line(task_id, line, stdstream)
            stdout = "Finished"
            stderr = ""
            rc = 0
        else:
            rc, stdout, stderr = cmd(args)

    except Exception as e:
        log.error(repr(e))
        stdout = ''
        stderr = f"FAILED: {str(e)}"
        rc = 1
    task_end(task_id, task_start, rc, stdout, stderr)


def calculate_task_name(cmd, params):
    if isinstance(params, dict):
        paramstring = " ,".join(['{}={}'.format(k, v)
                                 for k, v in params.items()])
    else:
        paramstring = " ,".join([str(a) for a in params])
    return f"{cmd.__name__}({paramstring})"


def _async_cmd_(command, obj, cmd=_cmd_):
    def calculate_timestamp():
        epoch = datetime.datetime.utcfromtimestamp(0)
        now = datetime.datetime.utcnow()
        timestamp = int((now - epoch).total_seconds() * 1000)
        return timestamp

    thread_id = calculate_timestamp()  # use ms id as identifier
    task_name = calculate_task_name(cmd, command)
    task_start(thread_id, obj, task_name)
    if cmd != _cmd_:
        log.debug(f"{cmd} {command}")
        submit_task(_python_cmd_, cmd, command, thread_id=thread_id)
    else:
        submit_task(cmd, command, obj, is_threaded=True, thread_id=thread_id)

    return None, str(thread_id), None


generic_success_filename = {'network': 'network_success.txt', 'route': 'network_success.txt',
                            'netcfg': 'network_success.txt'}


# pragma: no cover
def _mock_cmd_(command, obj='network'):
    try:
        if not command or len(command) < 3:
            raise IguardApiException('No command')
        cli_output_filename = f"cli_{command[1].replace('--', '')}_{command[2]}"
        if len(command) == 4 and command[3] == '--xml':
            cli_output_filename = f"{cli_output_filename}_{command[3].replace('--', '')}"
        cli_output_filename = f'{cli_output_filename}.txt'
        filename = os.path.join(os.environ.get('CLI_OUTPUT_DIR', const.CLI_OUTPUT_DIR),
                                cli_output_filename)
        if not os.path.exists(filename):
            filename = os.path.join(os.environ.get('CLI_OUTPUT_DIR', const.CLI_OUTPUT_DIR),
                                    generic_success_filename.get(obj, 'network_success.txt'))

        with open(filename, "r") as infile:
            response = infile.read()
        return 0, response, 0
    except Exception as e:
        if getattr(e, 'message', None):
            log.exception()
            raise IguardApiException(e)
        log.error(str(e))
        raise IguardApiException(str(e))


def transform_errors(out, only_first_error=False):
    errors = re.findall(r'.*^ERROR: (.*)$', out, flags=re.MULTILINE)
    if errors:
        message = errors[0] if only_first_error else ' '.join(errors)

    else:
        invalid = str.maketrans('', '', ''.join(
            [chr(char) for char in range(1, 32)]))
        message = out.translate(invalid)

    return message


def run_syscli(command: list, parser: Optional[Callable], obj):
    log.info(f"running syscli, command: {command} parser: {parser} object: {obj}")
    infiniguard_api_mock = os.environ.get('INFINIGUARD_API_MOCK', "0") == "1"

    fn = _mock_cmd_ if infiniguard_api_mock else _cmd_ if parser != parse_async else _async_cmd_
    rc, out, err = fn(command, obj)
    if rc:
        log.error(f"rc: {rc} out: {out} err: {err}")
        return_cli_err_msg = os.environ.get('RETURN_CLI_ERROR_MSG', "1") == "1"
        if return_cli_err_msg:
            if out:
                message = transform_errors(out, only_first_error=True)
            else:
                message = transform_errors(err)
        else:
            message = f"Received return code: {rc} from sub-process to CLI"
        raise IguardApiException(message)
    return parser(out) if parser else out


def run_python(args, cmd, obj):
    rc, out, err = _async_cmd_(args, obj, cmd=cmd)
    if rc:
        log.error(f"rc: {rc} out: {out} err: {err}")
        message = 'Received {} from thread to python command'.format(rc)
        raise IguardApiException(message)
    return out


def run_syscli1(op: str, obj: str, parser: Callable, *args, **kwargs):
    try:
        command_line = ['/opt/DXi/syscli', f'--{op}', obj] if op and obj else []
        command_line.extend([f'--{v}' for v in args])
        for (k, v) in kwargs.items():
            command_line.append(f'--{k}')
            command_line.append(f'{v}')
        result = run_syscli(command_line, parser, obj)
        return result, None
    except IguardApiException as e:
        log.exception("Exception on running syscli")
        if getattr(e, 'message', None):
            return None, str(e)
        else:
            return None, str(e)
    except Exception as e:
        log.exception("Unexpected exception on running syscli")
        return None, str(e)
