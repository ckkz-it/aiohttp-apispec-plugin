from aiohttp import web
from aiohttp.hdrs import METH_ALL
from aiohttp.web_urldispatcher import AbstractRoute
from apispec import BasePlugin, yaml_utils

from aiohttp_apispec_plugin.utils import issubclass_safe


class AioHttpPlugin(BasePlugin):
    """APISpec plugin for AioHttp"""
    view_uri_mapping: dict

    def __init__(self, app: web.Application):
        super().__init__()
        self.view_uri_mapping = self._generate_view_uri_mapping(app)

    def path_helper(self, view, operations, path=None, **kwargs):
        operations.update(yaml_utils.load_operations_from_docstring(view.__doc__) or {})
        path = path or self.view_uri_mapping[view]["uri"]

        methods = self.view_uri_mapping[view]["methods"]

        for method_name, method_handler in methods.items():
            docstring_yaml = yaml_utils.load_yaml_from_docstring(method_handler.__doc__)
            operations[method_name] = docstring_yaml or {}
        return path

    def _generate_view_uri_mapping(self, app: web.Application) -> dict:
        routes = app.router.routes()
        mapping = {}
        for route in routes:
            uri = self._get_uri(route)
            view = route.handler
            mapping[view] = {
                "uri": uri,
                "methods": {},
            }
            if issubclass_safe(route, web.View):
                for attr in dir(view):
                    if attr.upper() in METH_ALL:
                        mapping[view]["methods"][attr] = getattr(view, attr)
            else:
                method = route.method.lower()
                view = route.handler
                mapping[view]["methods"][method] = view

        return mapping

    def _get_uri(self, route: AbstractRoute) -> str:
        path_info = route.resource.get_info()
        return path_info.get("path") or path_info.get("formatter")
