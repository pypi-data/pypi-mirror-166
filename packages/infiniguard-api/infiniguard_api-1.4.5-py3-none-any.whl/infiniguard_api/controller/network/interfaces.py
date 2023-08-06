"""
Endpoint: /network/interfaces/

Methods: POST, GET, PATCH, DELETE

CLI Commands:
    syscli --add netcfg --devname <DEVNAME> [--dhcp]|[--ipaddr <IPADDR> --netmask <NETMASK> --gateway <GATEWAY>]
        [--mtu <SIZE>] [--defaultgw YES] [--segments REP,MGMT,DATA] [--nat <NAT_IPADDR>] [--hosts <IP1,IP2,IP3>]
        [--extHostIp YES] [--slaves <DEV1>,<DEV2>,<...>] [--mode RR|AB|LACP] [--sure]
    syscli --edit netcfg --devname <DEVNAME> [--mtu <SIZE>] [--mode RR|AB|LACP] [--slaves <DEV1>,<DEV2>,<...>]
        [--nat <NAT_IPADDR>|none] [--extHostIp YES|NO] [--sure]
    syscli --del netcfg --devname <DEVNAME> [--sure]

"""
from collections import OrderedDict

from marshmallow import ValidationError

from infiniguard_api.controller.network import host
from infiniguard_api.controller.network.list_interface_xml import build_response
from infiniguard_api.lib.hw.cli_handler import run_syscli1
from infiniguard_api.lib.hw.output_parser import check_command_successful, parse_list_interface
from infiniguard_api.lib.iguard_api_exceptions import IguardApiWithCodeException
from infiniguard_api.lib.logging import iguard_logging
from infiniguard_api.lib.rest.common import (
    build_error_message,
    build_entity_response,
    build_error_model, http_code, requires_reboot,
    build_empty_response,
)
from infiniguard_api.model.validators import validate_intfname, MIN_INTF, MAX_INTF

log = iguard_logging.get_logger(__name__)


def _get_available_intf_id(devname):
    """
    Returns the smallest available interface ID for the given device name.
    If the device name is p4p1, and the existing interfaces are p4p1:1 and p4p1:3, will return 2.
    If no interface exists for the device name, returns 1
    """
    response, qualifier, code = retrieve_interface({})

    if code != http_code.OK:
        error = dict(error=dict(message=[response], code='SYSTEM_ERROR'))
        raise IguardApiWithCodeException(
            error, http_code.INTERNAL_SERVER_ERROR)

    if not response:
        return MIN_INTF

    result = response.get('result', [])
    intf_ids = [int(intf['intfname'].split(':')[1]) for intf in result if intf.get('devname') == devname and
                intf.get('intfname') and ':' in intf['intfname']]
    if not intf_ids:
        return MIN_INTF

    intf_ids.sort()

    max_intf = intf_ids[-1] + 1
    for i in range(1, max_intf):
        if i not in intf_ids:
            return i

    return max_intf


def generate_intfname(full_devname, vlan_id=None):
    intf_id = None

    if ':' in full_devname:
        devname_part, intf_id = full_devname.split(':')
    else:
        devname_part = full_devname

    if '.' in devname_part:
        devname, vlan_id = devname_part.split('.')
    else:
        devname = devname_part

    if not intf_id:
        intf_id = _get_available_intf_id(devname)

    return f'{devname}.{vlan_id}:{intf_id}' if vlan_id else f'{devname}:{intf_id}', vlan_id, intf_id


def filter_intf_by_intfname(name, data):
    """
    Filter an array of processed data from syscli by either the full interface name
    or by the devname if it is not an interface name (recognized by not having :1)
    Args:
        name: interface name of form devname[.vlanid]:interface_number or devname
        data: array of processed cli data

    Returns:
        array (1 or more) if input if devname or else a dictionary
    """
    parts = name.split(':')
    num_parts = len(parts)
    if num_parts > 2:
        raise ValidationError(
            "interfaces must be of the format: devname.vlanid:interface_number")
    # vlanid with no interface number
    if num_parts == 1 and len(parts[0].split('.')) > 1:
        raise ValidationError("vlanid provided with no interface number")
    check_field = 'intfname' if num_parts == 2 else 'devname'
    data = [d for d in data if d.get(check_field, None) == name]
    if check_field == 'intfname':
        if len(data) > 1:
            error = dict(error=dict(message=[
                'only one interface with name: {} can exist'.format(name)], code='SYSTEM_ERROR'))
            raise IguardApiWithCodeException(
                error, http_code.INTERNAL_SERVER_ERROR)
        return data[0] if data else {}
    return data


@requires_reboot('Changing the network configuration requires a system reboot.')
def create_interface(**request):
    """
    Command:
        syscli --add netcfg --devname <DEVNAME> [--dhcp]|[--ipaddr <IPADDR> --netmask <NETMASK> --gateway <GATEWAY>]
            [--mtu <SIZE>] [--defaultgw YES] [--segments REP,MGMT,DATA] [--nat <NAT_IPADDR>] [--hosts <IP1,IP2,IP3>]
            [--extHostIp YES] [--slaves <DEV1>,<DEV2>,<...>] [--mode RR|AB|LACP] [--sure]

    Args:
        request: model.network.CreateInterfaceSchema

    Returns:
        response: model.network.InterfaceResponse
        code: HTTP Status Code

    Examples:
        {
            "ext_dde_ip": False,
            "gateway": "5.6.7.8",
            "devname": "p7p1",
            "vlan": 22,
            "ip_address": "1.2.3.4",
            "mtu": 9000,
            "netmask": "255.255.255.0",
            "interface_type": 'Port',
            "traffic_type": ['data', 'replication']
        }
    """
    try:
        if request.get('errors'):
            error = dict(error=dict(message=build_error_message(
                request['errors']), code='BAD_REQUEST'))
            raise IguardApiWithCodeException(error, http_code.BAD_REQUEST)

        command_params = request

        # syscli's devname param refers to the entire interface name, with intf ID and vlan ID
        full_intfname, vlan_id, intf_id = generate_intfname(request['devname'], request.pop('vlan', None))
        if int(intf_id) > MAX_INTF:
            error = dict(message=f"A maximum of {MAX_INTF} IP addresses per port are allowed",
                         code='NETWORK_CONFIGURATION_ERROR')
            raise IguardApiWithCodeException(
                error, http_code.CONFLICT)

        command_params['devname'] = full_intfname

        if request.get('extHostIp') == 'YES':
            host.set_default_gateway(request['gateway'])

        result, errmsg = run_syscli1(
            'add', 'netcfg', check_command_successful, 'sure', **command_params)
        if not result:
            error = dict(message=errmsg, code='NETWORK_CONFIGURATION_ERROR')
            raise IguardApiWithCodeException(
                error, http_code.INTERNAL_SERVER_ERROR)

        response, qualifier, code = retrieve_interface({'name': full_intfname})
        if code != http_code.OK or not response or not isinstance(response.get('result'), dict):
            error = build_error_model(
                error_message=build_error_message(
                    {
                        'create_interface': f"Creation command returned successfully, "
                                            f"but no {full_intfname} interface was found"
                    }),
                error_code='INTERFACE_NOT_FOUND')
            return build_entity_response(error=error), http_code.INTERNAL_SERVER_ERROR

        return response, http_code.CREATED

    except IguardApiWithCodeException as e:
        log.exception("Exception on interface creation")
        return build_entity_response(error=e.error), e.code
    except Exception as e:
        error = dict(error=dict(
            message=[getattr(e, 'message', str(e))], code='UNEXPECTED_EXCEPTION'))
        log.exception("Unexpected exception on interface creation")
        return error, http_code.INTERNAL_SERVER_ERROR


def _convert_segments(data):
    """
    Converts the segments field according to the syscli requirement
    If 'any' is in the list nothing is passed to the syscli, as all traffic types is the default
    """
    name_mapping = {'replication': 'REP', 'data': 'DATA'}

    if 'segments' in data:
        if 'any' in data['segments']:
            del data['segments']
        else:
            data['segments'] = ','.join(name_mapping[option] for option in data['segments'])

    return data


def convert_from_request(data):
    try:
        if data.pop('ext_host_ip', False):
            data['extHostIp'] = 'YES'

        # The syscli argument is called ipaddr, but when the data returns it returns as "IP Address"
        if 'ip_address' in data:
            data['ipaddr'] = data.pop('ip_address')

        if data.get('type', '').lower() == 'bond':
            data['slaves'] = ','.join(data['slaves'])
            data.setdefault('mode', 'RR')

        _convert_segments(data)
        data.pop('type', None)  # interface_type is only used internally - it isn't a syscli param

        return data

    except Exception as e:
        raise ValidationError(message=str(e))


def convert_to_response(data):
    """Convert the result of the

    Args:
        data: gets a JSON array of dicts containing interface config in CLI format

    Returns:
        array of model.network.InterfaceSchema

    """
    try:
        translate_map = {
            "device_name": "devname", "connection": "carrier", "state": "operstate",
            "interface_name": "intfname", "exthostip": "ext_host_ip", "nat_ip_address": "nat"
        }
        rdata = []
        for d in data:
            stop = False
            if not d or not isinstance(d, OrderedDict):
                stop = True
            if d.get('type', None) == 'Port' and not d.get('device_name', '').startswith('p'):
                stop = True
            if d.get('type', None) == 'Bond':
                for s in d.get('slaves', []):
                    if not s.startswith('p'):
                        stop = True
                        break
            if stop:
                continue
            rd = {translate_map.get(k, k): v for k, v in d.items()}
            rd['ext_host_ip'] = rd.get('ext_host_ip', False) == 'YES'
            rd['configured'] = rd.get('configured', False) == 'true'
            rd.pop('default_gateway', None)
            rd['segments'] = [r['segment'] for r in rd.get('segments', [])]
            for r in rd.get('routes', []):
                if r['destination']:
                    r['network'] = r.pop('destination')
            rdata.append(rd)
        discard_keys = ['boot_protocol', 'maximum_speed']
        [r.pop(key, None) for key in discard_keys for r in rdata]
        return rdata
    except Exception as e:
        raise ValidationError(message=str(e))


def retrieve_interface(request):
    """
    Command:
        syscli --list interface --xml

    Args:
        request: None or dict with key 'name'

    Returns:
        response: model.network.LogicalInterfacePaginatedSchema or model.network.LogicalInterfacesPaginatedSchema
        qualifier: "object" or "list"
        code: HTTP Status Code

    Examples:
        request: None
        response:
            [{
                "intfname": "bond0.10:1",
                "ip_address": "10.10.8.7",
                "mask": "255.255.255.0",
                "gateway": "10.10.8.7",
                "default_gateway": "NO",
                "segments": ["DATA"],
                "ext_host_ip": "NO",
                "devname": "bond0"
            },
            {
                "intfname": "p1p1:1",
                "ip_address": "1.2.3.4",
                "mask": "255.255.255.0",
                "gateway": "1.2.3.4",
                "default_gateway": "NO",
                "segments": ["ALL"],
                "ext_host_ip": "NO",
                "devname": "p1p1"
            }]

            {
                "intfname": "p1p2.10:1",
                "ip_address": "10.11.12.13",
                "mask": "255.255.255.0",
                "gateway": "10.11.12.1",
                "default_gateway": "NO",
                "segments": ["ALL"],
                "default_gateway": "NO",
                "ext_host_ip": "NO",
                "devname": "p1p2"
            }

        request: {"name": "bond0.10:1"}
        response:
            {
                "intfname": "bond0.10:1",
                "ip_address": "10.10.8.7",
                "mask": "255.255.255.0",
                "gateway": "10.10.8.7",
                "default_gateway": "NO",
                "segments": ["DATA"],
                "ext_host_ip": "NO",
                "devname": "bond0"
            }

    """
    try:
        data, errmsg = run_syscli1('list', 'interface', parse_list_interface)
        if errmsg:
            error = dict(error=dict(message=[errmsg], code='SYSTEM_ERROR'))
            return error, None, http_code.INTERNAL_SERVER_ERROR

        data = convert_to_response(data)
        if request.get('name', None):
            try:
                validate_intfname(request['name'], only_intf=True)
            except ValidationError as e:
                error = build_error_model(
                    error_message=build_error_message(
                        {'retrieve_interface': e.messages}),
                    error_code='BAD_REQUEST')
                return build_entity_response(error=error), 'object', http_code.BAD_REQUEST

            data = filter_intf_by_intfname(request['name'], data)
            if not data:
                error = build_error_model(
                    error_message=build_error_message(
                        {'retrieve_interface': 'Interface not found'}),
                    error_code='INTERFACE_NOT_FOUND')
                return build_entity_response(error=error), 'object', http_code.NOT_FOUND

        return build_response(request, data)
    except IguardApiWithCodeException as e:
        log.error(e.error)
        return e.error, None, e.code
    except Exception as e:
        error = dict(error=dict(
            message=[getattr(e, 'message', str(e))], code='UNEXPECTED_EXCEPTION'))
        log.error(error)
        return error, None, http_code.INTERNAL_SERVER_ERROR


@requires_reboot('Changing the network configuration requires a system reboot.')
def update_interface(**request):
    """
    Command:
        syscli --edit netcfg --devname <DEVNAME> [--mtu <SIZE>] [--nat <NAT_IPADDR>] [--extHostIp YES] [--sure]

    Args:
        request: model.network.LogicalInterfaceSchema

    Returns:
        response: model.network.LogicalInterfacePaginatedSchema
        code: HTTP Status Code

    Examples:
        {
            "nat": "192.168.1.200",
             "ext_dde_ip": True,
        }

    """
    try:
        if request.get('errors', None):
            error = dict(error=dict(message=build_error_message(
                request['errors']), code='BAD_REQUEST'))
            log.error(error)
            return error, http_code.BAD_REQUEST

        netcfg_args = request
        full_intfname = request.pop('name')
        netcfg_args['devname'] = full_intfname

        current_intf, qualifier, code = retrieve_interface(
            {'name': full_intfname})
        if code != http_code.OK or not current_intf or not isinstance(current_intf.get('result', None), dict):
            error = build_error_model(
                error_message=build_error_message({'update_interface': 'Interface not found'}),
                error_code='INTERFACE_NOT_FOUND')
            return build_entity_response(error=error), http_code.NOT_FOUND

        if request.get('extHostIp') == 'YES':
            host.set_default_gateway(current_intf['result']['gateway'])

        result, errmsg = run_syscli1(
            'edit', 'netcfg', check_command_successful, 'sure', **netcfg_args)
        if not result:
            error = dict(message=errmsg, code='NETWORK_CONFIGURATION_ERROR')
            raise IguardApiWithCodeException(
                error, http_code.INTERNAL_SERVER_ERROR)

        response, qualifier, code = retrieve_interface({'name': full_intfname})
        if code != http_code.OK or not response or not isinstance(response.get('result'), dict):
            error = build_error_model(
                error_message=build_error_message(
                    {
                        'update_interface': f"Update command returned successfully, "
                                            f"but no {netcfg_args['intf_id']} interface was subsequently found"
                    }),
                error_code='INTERFACE_NOT_FOUND')
            return build_entity_response(error=error), http_code.INTERNAL_SERVER_ERROR

        return response, http_code.OK

    except IguardApiWithCodeException as e:
        log.exception("Exception on interface creation")
        return build_entity_response(error=e.error), e.code
    except Exception as e:
        error = dict(error=dict(
            message=[getattr(e, 'message', str(e))], code='UNEXPECTED_EXCEPTION'))
        log.exception("Unexpected exception on interface creation")
        return error, http_code.INTERNAL_SERVER_ERROR


@requires_reboot('Changing the network configuration requires a system reboot.')
def delete_interface(**request):
    """
    Command:
        syscli --del netcfg --devname <DEVNAME> [--sure]

    Args:
        name: Full device name of L3 interface

    Returns:
        data: model.base_schema.MessageSchema
        code: HTTP Status Code
    """
    try:
        intf_name = request.pop('name')

        result, qualifier, code = retrieve_interface(
            {'name': intf_name})
        if code != http_code.OK or not result or not isinstance(result.get('result', None), dict):
            error = build_error_model(
                error_message=build_error_message({'delete_interface': 'Interface not found'}),
                error_code='INTERFACE_NOT_FOUND')
            return build_entity_response(error=error), http_code.NOT_FOUND

        netcfg_args = ['sure']
        netcfg_kwargs = {'devname': intf_name}
        result, errmsg = run_syscli1(
            'del', 'netcfg', check_command_successful, *netcfg_args, **netcfg_kwargs)
        if not result:
            error = dict(message=[errmsg], code='NETWORK_CONFIGURATION_ERROR')
            return dict(error=error), http_code.INTERNAL_SERVER_ERROR

        return build_empty_response(), http_code.OK
    except Exception as e:
        error = dict(error=dict(
            message=[getattr(e, 'message', str(e))], code='UNEXPECTED_EXCEPTION'))
        log.exception("Unexpected exception on interface creation")
        return error, http_code.INTERNAL_SERVER_ERROR


def verify_same_gateway(intf_dict):
    """
    If extHostIp is YES or is also being updated, check that the new ip address and/or default gateway
    belong to same subnet as the host default gateway. If not, return False else return True.

    Args:
        intf_dict: request info

    Returns:
        True or False
    """
    try:
        if not intf_dict.get('host_ext_ip', False):
            return True

        response, qualifier, code = retrieve_interface(
            {'name': intf_dict['devname']})
        if code != http_code.OK or not response or not isinstance(response.get('result', None), dict):
            error = dict(error=dict(
                message=['Error retrieving interface'], code='SYSTEM_ERROR'))
            raise IguardApiWithCodeException(
                error, http_code.INTERNAL_SERVER_ERROR)

        intf = response['result']
        if not intf.get('ext_host_ip', False):
            return True

        response, qualifier, code = host.retrieve_host({})
        if code != http_code.OK or not response or not response.get('result', None):
            error = dict(error=dict(message=[errmsg], code='SYSTEM_ERROR'))
            raise IguardApiWithCodeException(
                error, http_code.INTERNAL_SERVER_ERROR)

        network = response['result']
        default_gateway = network.get('default_gateway', None)
        if not default_gateway:
            return True

        return True
    except IguardApiWithCodeException as e:
        log.error(e.error)
        return e.error, e.code
    except Exception as e:
        log.error(e.message)
        return False
