import re
from typing import Tuple, Optional

from infiniguard_api.common.const import INFINIDAT_ROLE, ADMIN_ROLE
from infiniguard_api.controller.network.list_interface_xml import build_response
from infiniguard_api.lib.hw.cli_handler import run_syscli1, run_syscli
from infiniguard_api.lib.hw.output_parser import check_command_successful_reboot_required, \
    parse_list_interfaces_all
from marshmallow import ValidationError
from infiniguard_api.lib.logging import iguard_logging
from infiniguard_api.lib.rest.common import (build_entity_response,
                                             build_error_model, http_code, build_empty_response, requires_reboot,
                                             allowed_roles, build_error_response)
from infiniguard_api.model.network import EthernetPortBaseSchema


log = iguard_logging.get_logger(__name__)

CUSTOMER_ETHERNET_PORT_PATTERN = '^p\dp\d$|bond\d$'


def get_ethernet_ports(**request) -> Tuple[dict, Optional[str], int]:
    """Endpoint:
        /network/ports/
        /network/ports/<name>

    CLI Command:
        syscli --list interface

    Args:
        request: None or dict with key 'name'

    Returns:
        response: model.network.EthernetPortResponseSchema or model.network.EthernetPortsResponseSchema
        qualifier: "object" or "list"
        code: HTTP Status Code

    """
    ethernet_port_name = request.get('name', '')
    data, errmsg = run_syscli1('list', 'interface', parse_list_interfaces_all)
    if not errmsg and data:
        try:
            validated_data = EthernetPortBaseSchema().load(data=data, many=True)
        except ValidationError as e:
            log.exception('ethernet ports model validation exception')
        else:
            result = [v for v in validated_data
                      if re.match(CUSTOMER_ETHERNET_PORT_PATTERN, v['device_name'])]
            if ethernet_port_name:
                result = next((x for x in result if x['device_name'] == ethernet_port_name), None)
                if not result:
                    error = build_error_model(
                        error_message='Ethernet port not found',
                        error_code='ETHERNET_PORT_NOT_FOUND')
                    return build_error_response(error=error), None, http_code.NOT_FOUND
            return build_response(request, result)

    error = build_error_model(
        error_message='Unable to retrieve ethernet ports',
        error_code='INTERNAL_ERROR')
    return build_error_response(error=error), None, http_code.INTERNAL_SERVER_ERROR


def _validate_non_bond_fields(slaves, mode, devname):
    invalid_non_bond_fields = []
    if slaves and not devname.startswith('bond'):
        invalid_non_bond_fields.append('slaves')
    if mode and not devname.startswith('bond'):
        invalid_non_bond_fields.append('mode')

    if invalid_non_bond_fields:
        return build_error_model(
            error_message=f'"[{", ".join(invalid_non_bond_fields)}]" are not valid fields '
                          f'for the ethernet port "{devname}"',
            error_code='WRONG_FIELDS')
    return None


def _operation_failed_response(devname, out, operation):
    error_message = f'Error {operation} ethernet port "{devname}" details: {" ".join(out) if out else "N/A"}'
    log.error(error_message)
    error = build_error_model(
        error_message=error_message,
        error_code='INTERNAL_ERROR')
    return build_error_response(error=error), http_code.INTERNAL_SERVER_ERROR


@requires_reboot('Updating the ethernet ports configuration requires a system reboot.')
@allowed_roles(roles=[INFINIDAT_ROLE, ADMIN_ROLE])
def update_ethernet_port(**request) -> Tuple[dict, int]:
    response, _, code = get_ethernet_ports(**request)
    if code != 200:
        return response, code
    ex_port = response['result']
    devname, mtu, slaves, mode = request['name'], request.get('mtu'), request.get('slaves'), request.get('mode')
    if not ex_port['configured']:

        if ex_port['type'] == 'Slave':
            error_message = f'Error updating ethernet port "{devname}", ' \
                            f'operation on a type bond is not permitted.'
        else:
            error_message = f'Error updating ethernet port "{devname}", ' \
                            f'operation on non-configured port is not permitted.'
        error = build_error_model(
            error_message=error_message,
            error_code='ETHERNET_PORT_UPDATE_CONFLICT')
        return build_error_response(error=error), http_code.CONFLICT
    validation_error = _validate_non_bond_fields(slaves, mode, devname)
    if validation_error:
        return build_error_response(error=validation_error), http_code.BAD_REQUEST

    command = ['/opt/DXi/syscli', '--edit', 'netcfg', '--sure', '--devname', devname]
    if mtu:
        command.extend(['--mtu', str(mtu)])
    if slaves:
        command.extend(['--slaves', ','.join(slaves)])
    if mode:
        command.extend(['--mode', mode])

    success, reboot_required, out = run_syscli(command,
                                               check_command_successful_reboot_required,
                                               'editnetcfg')
    if not success:
        return _operation_failed_response(devname, out, 'updating')
    return build_empty_response(), http_code.ACCEPTED


def _get_requires_approval_delete(**request):
    devname: str = request['name']
    return f'You are about to delete ethernet port "{devname}"'


@requires_reboot('Deleting the bond port requires a system reboot.')
@allowed_roles(roles=[INFINIDAT_ROLE, ADMIN_ROLE])
def delete_ethernet_port(**request) -> Tuple[dict, int]:
    response, _, code = get_ethernet_ports(**request)
    if code != 200:
        return response, code
    devname = request['name']
    if not devname.startswith('bond'):
        error = build_error_model(error_message=f'Error deleting ethernet port "{devname}" '
                                                f'is a physical device and cannot be deleted',
                                  error_code='ETHERNET_PORT_DELETE_CONFLICT')
        return build_error_response(error=error), http_code.CONFLICT

    command = ['/opt/DXi/syscli', '--del', 'netcfg', '--sure', '--devname', devname]
    success, reboot_required, out = run_syscli(command,
                                               check_command_successful_reboot_required,
                                               'delnetcfg')
    if not success:
        return _operation_failed_response(devname, out, 'deleting')
    return build_empty_response(), http_code.ACCEPTED
