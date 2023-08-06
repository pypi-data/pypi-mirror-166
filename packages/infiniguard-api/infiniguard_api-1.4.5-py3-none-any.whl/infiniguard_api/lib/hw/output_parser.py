import re
import copy
from typing import Tuple, List

import xmltodict
from collections import OrderedDict
from configobj import ConfigObj
from six.moves import StringIO, configparser

from infiniguard_api.lib.hw.netlib import generate_patch_panel_ports_mapping
from infiniguard_api.lib.logging import iguard_logging

log = iguard_logging.get_logger(__name__)


def convert_to_nested_config(data):
    def remap(l):
        n = (len(l) - len(l.lstrip())) // 2
        l1 = (l.replace('[', '[' * n).replace(']', ']' * n) if n and '[' in l else copy.copy(l)).strip()
        return l1

    return [remap(line) for line in data.split('\n')]


def normalize_config(input_config):
    newinput = list()
    for dictionary in input_config:
        newdict = dict()
        for k, v in dictionary.items():
            if str(v).lower() in ['disabled', 'false', 'off', 'no']:
                v = False
            elif str(v).lower() in ['enabled', 'true', 'on', 'yes']:
                v = True
            newdict[k] = v
        newinput.append(newdict)
    return newinput


def parse_config_style_raw(out):
    if isinstance(out, bytes):
        out = out.decode()
    config = configparser.ConfigParser(allow_no_value=True)
    out = '[total]\n' + '\n'.join([a.strip() for a in out.split('\n') if '=' in a])
    buf = StringIO(out)
    config.readfp(buf)
    res = [
        b for (a, b) in
        list({s: {k.lower().replace(' ', '_'): v for k, v in config.items(s)} for s in config.sections()}.items())
    ]
    result = normalize_config(res)
    log.debug(f"Command Output: {result}")
    return result


def parse_config_style(out):
    if isinstance(out, bytes):
        out = out.decode()
    config = configparser.ConfigParser(allow_no_value=True)
    out = '[total]\n' + '\n'.join([a.strip() for a in out.split('\n') if '=' in a])
    buf = StringIO(out)
    config.readfp(buf)
    config.remove_section('total')
    res = [
        b for (a, b) in
        list({s: {k.lower().replace(' ', '_'): v for k, v in config.items(s)} for s in config.sections()}.items())
    ]
    result = normalize_config(res)
    log.debug(f"Command Output: {result}")
    return result


def parse_list_user(out):
    return parse_config_style(out)


def parse_list_interface_xml(out):
    if isinstance(out, bytes):
        out = out.decode()
    try:
        result = xmltodict.parse(''.join(re.findall(r'^\s*<.*>\n?', out, flags=re.MULTILINE)),
                                 force_list=('DNS_Servers', 'CustomerInterface', 'Interface', 'L3Interface', 'Slave',
                                             'StaticRoute'))
        log.debug(f"Parser parse_list_interface_xml result: {result}")
        return result
    except Exception:
        log.exception("parse_list_interface_xml error")
        return []


def listify(d):
    """
    Convert a nested dict to an array of dicts that are at the sam level
    Args:
        d:

    Returns:

    """
    listd = OrderedDict()
    for k, v in d.items():
        if not ('=' in k and isinstance(v, dict)):
            listd[k] = v
        else:
            listv = listify(v)
            pre = k.split('=')[0].rstrip(' s') + 's'
            if listd.get(pre):
                listd[pre].append(listv)
            else:
                listd[pre] = [listv]
    return listd


def process_list_interface(data: OrderedDict) -> list:
    data = data.pop('devices', [])
    rdata = []
    for d in data:
        for i in d.get('interfaces', []):
            rd = copy.deepcopy(d)
            rd.pop('interfaces', None)
            rd.update(i)
            rdata.append(rd)
    log.debug(f"process_list_interface result: {data}")
    return rdata


def process_list_interfaces_all(data: OrderedDict) -> list:
    """
    Parse network interfaces and add patch panel port number from frontend ethernet ports.
    """
    updated_data = []
    data = data.pop('devices', [])
    ports_mapping = generate_patch_panel_ports_mapping(data)
    for port in data:
        pp_port = ports_mapping.get(port['device_name'])
        if pp_port:
            port['patch_panel'] = pp_port
        updated_data.append(port)
    return updated_data


def process_list_hostmapping(data):
    data = data.pop('groups', [])
    rdata = []
    for d in data:
        devices = d.pop('devices', None)
        if devices:
            vmcs = 0
            vtds = 0
            for i in devices:
                dtype = i.get('type', None)
                if dtype == 'VMC':
                    vmcs += 1
                elif dtype == 'VTD':
                    vtds += 1
            d['devices'] = '{} VMC, {} VTD'.format(vmcs, vtds)
        rdata.append(d)
    log.debug(f"Command Result:{data}")
    return rdata


def parse_list_interface(out) -> list:
    return parse_list_nested_data(out, process_list_interface)


def parse_list_interfaces_all(out) -> list:
    return parse_list_nested_data(out, process_list_interfaces_all)


def parse_list_hostmapping(out):
    return parse_list_nested_data(out, process_list_hostmapping)


def parse_list_nested_data(out, processor):
    def pre(l):
        l1 = ('# ' + l) if '=' not in l or any(x in l for x in ['Total interface count', 'Total count', ]) else l
        return l1

    def post(conf):
        fn = lambda s, k: s.rename(k, k.lower().replace(' = ', '=').translate(str.maketrans(' -', '__')))
        conf.walk(fn, call_on_sections=True)
        result = listify(conf)
        return result

    if isinstance(out, bytes):
        out = out.decode()
    data = convert_to_nested_config(out)
    data = [pre(line) for line in data]
    buf = StringIO('\n'.join(data))
    config = ConfigObj(buf, write_empty_values=True)
    data = post(config)
    return processor(data)


def parse_single_entry(out):
    if isinstance(out, bytes):
        out = out.decode()
    config = configparser.ConfigParser(allow_no_value=True)
    out = '[objects]\n' + '\n'.join([a.strip() for a in out.split('\n') if '=' in a])
    buf = StringIO(out)
    config.readfp(buf)
    result = [
        b for (a, b) in
        list({s: {k.lower().replace(' ', '_'): v for k, v in config.items(s)} for s in config.sections()}.items())
    ]
    log.debug(f"Command Output: {result}")
    return result[0]


def parse_accentstats(out):
    if isinstance(out, bytes):
        out = out.decode()
    config = configparser.ConfigParser(allow_no_value=True)
    out = '\n'.join([re.sub(r"(?i)^.*Accent Statistics:.*$",
                            "[accent_statistics]", a) for a in out.split('\n')])
    out = '\n'.join([re.sub(r"(?i)^.*Optimized Duplication Statistics:.*$",
                            "[optimized_duplication_tatistics]", a) for a in out.split('\n')])
    out = '[basic_statistics]\n' + '\n'.join(
        [a.strip() for a in out.split('\n') if (('=' in a or '[' in a) and 'Total count' not in a)])
    buf = StringIO(out)
    config.readfp(buf)
    result = [{s: {k.lower().replace(' ', '_'): v for k, v in config.items(s)} for s in config.sections()}]
    log.debug(f"Command Output: {result}")
    return result


def check_command_successful(out):
    if isinstance(out, bytes):
        out = out.decode()
    match = re.search(r'^.*Command completed successfully.*\n?', out, flags=re.MULTILINE)
    log.debug(f"Successful: {match is not None}, Result Message: {out}")
    return match is not None, out.split('\n')


def check_command_successful_reboot_required(out) -> Tuple[bool, bool, List[str]]:
    match_success, check_command_out = check_command_successful(out)
    match_reboot = re.search(r'^In order for changes to take effect the system must be rebooted.',
                             out, flags=re.MULTILINE)
    return match_success is not None, match_reboot is not None, check_command_out


def parse_async(out):
    if isinstance(out, bytes):
        out = out.decode()
    return out
