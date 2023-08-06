from flask_apispec import (
    MethodResource,
    doc,
    marshal_with,
    use_kwargs
)

from infiniguard_api.common.messages import paginated_params_desc
from infiniguard_api.controller.network.ethernet_ports import get_ethernet_ports, update_ethernet_port, \
    delete_ethernet_port
from infiniguard_api.lib.documentation import ddoc
from infiniguard_api.lib.rest.common import http_code
from infiniguard_api.model.base_schema import ErrorResponseSchema, EmptyResponseSchema, ForbiddenErrorResponseSchema, \
    ConflictErrorResponseSchema
from infiniguard_api.model.network import (EthernetPortsResponseSchema,
                                           EthernetPortResponseSchema,
                                           EthernetPortUpdateSchema, RebootRequiredSchema
                                           )
from infiniguard_api.view.network.common import network_api


@ddoc
class EthernetPortsResource(MethodResource):
    """
    :Methods: GET
    :Tags: Ethernet Ports

    """

    @ddoc
    @doc(operationId='get_ethernet_ports')
    @doc(params=paginated_params_desc)
    @marshal_with(EthernetPortsResponseSchema, code=http_code.OK, description="EthernetPortsResponseSchema on success")
    @marshal_with(ErrorResponseSchema, description="ErrorResponseSchema on failure")
    def get(self, **kwargs):
        """
        :Summary: Return all ethernet ports (pXpX, or bondX)
        """
        response, _qualifier, code = get_ethernet_ports(**kwargs)
        return response, code


@ddoc
class EthernetPortResource(MethodResource):
    """
    :Methods: GET, PUT, DELETE
    :Tags: Ethernet Ports
    """

    @ddoc
    @doc(operationId='get_ethernet_port')
    @doc(params=paginated_params_desc)
    @doc(params={
        'name':
            {
                'in': 'path',
                'type': 'string',
                'x-example': 'p4p4:1',
                'name': 'name',
                'required': True
            }
    })
    @marshal_with(EthernetPortResponseSchema, code=http_code.OK, description="EthernetPortResponseSchema on success")
    @marshal_with(ErrorResponseSchema, description="ErrorResponseSchema on failure")
    def get(self, **kwargs):
        """
        :Summary: Return the specified ethernet port
        """
        response, _qualifier, code = get_ethernet_ports(**kwargs)
        return response, code

    @ddoc
    @doc(operationId='update_ethernet_port')
    @doc(params={
        'name':
            {
                'in': 'path',
                'type': 'string',
                'x-example': 'p4p4:1',
                'name': 'name',
                'required': True
            }
    })
    @use_kwargs(EthernetPortUpdateSchema)
    @marshal_with(EmptyResponseSchema, code=http_code.ACCEPTED,
                  description="EmptyResponseSchema on success")
    @marshal_with(ConflictErrorResponseSchema, code=http_code.CONFLICT,
                  description="ConflictErrorResponseSchema on conflict")
    @marshal_with(ForbiddenErrorResponseSchema, code=http_code.FORBIDDEN,
                  description="ForbiddenErrorResponseSchema on forbidden")
    @marshal_with(ErrorResponseSchema, description="ErrorResponseSchema on failure")
    def put(self, **kwargs):
        """
        :Summary: Update the ethernet port configuration
        """
        response, code = update_ethernet_port(**kwargs)
        return response, code

    @ddoc
    @doc(operationId='delete_ethernet_port')
    @doc(params={
        'name':
            {
                'in': 'path',
                'type': 'string',
                'x-example': 'bond0',
                'name': 'name',
                'required': True
            }
    })
    @use_kwargs(RebootRequiredSchema)
    @marshal_with(EmptyResponseSchema, code=http_code.ACCEPTED,
                  description="EmptyResponseSchema on success")
    @marshal_with(ConflictErrorResponseSchema, code=http_code.CONFLICT,
                  description="ConflictErrorResponseSchema on conflict")
    @marshal_with(ForbiddenErrorResponseSchema, code=http_code.FORBIDDEN,
                  description="ForbiddenErrorResponseSchema on forbidden")
    @marshal_with(ErrorResponseSchema, description="ErrorResponseSchema on failure")
    def delete(self, **kwargs):
        """
        :Summary: Delete the ethernet port configuration
        """
        response, code = delete_ethernet_port(**kwargs)
        return response, code


ethernet_ports_view_func = EthernetPortsResource.as_view('ethernet_ports')
ethernet_port_view_func = EthernetPortResource.as_view('ethernet_port')

network_api.add_url_rule(
    'ethernet_ports/', view_func=ethernet_ports_view_func, methods=['GET'])
network_api.add_url_rule('ethernet_ports/<string:name>',
                         view_func=ethernet_port_view_func, methods=['GET', 'PUT', 'DELETE'])

