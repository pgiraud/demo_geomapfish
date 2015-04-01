from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPForbidden
from c2cgeoportal.views.proxy import Proxy
from c2cgeoportal.lib.filter_capabilities import (
    get_protected_layers,
    get_private_layers,
)
import logging

log = logging.getLogger(__name__)

class PrintProxy(Proxy):

    def __init__(self, request):
        Proxy.__init__(self, request)

    @view_config(route_name='file_proxy')
    def file_proxy(self):
        layer = self.request.matchdict.get('layer')
        file = self.request.matchdict.get('file')

        role_id = None if self.request.user is None else \
            self.request.user.role.id

        if layer in get_private_layers() and \
                layer not in get_protected_layers(role_id):
            raise HTTPForbidden

        functionalities = self.request.registry.settings.get('functionalities',
            {})
        url_prefix = functionalities['file_server_url']

        resp, content = self._proxy('%s/%s/%s' % (url_prefix, layer, file))
        headers = {}
        if 'content-type' in resp:
            headers['content-type'] = resp['content-type']
        if 'content-disposition' in resp:
            headers['content-disposition'] = resp['content-disposition']

        return Response(content, status=resp.status, headers=headers)
