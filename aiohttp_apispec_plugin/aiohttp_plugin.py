from aiohttp import web
from aiohttp.hdrs import METH_ALL
from aiohttp.web_urldispatcher import AbstractRoute
from apispec import BasePlugin, yaml_utils

from aiohttp_apispec_plugin.utils import issubclass_safe


class AioHttpPlugin(BasePlugin):
    """APISpec plugin for aiohttp"""
    resource_uri_mapping: dict

    def __init__(self, app: web.Application):
        super().__init__()
        self.resource_uri_mapping = self._generate_resource_uri_mapping(app)

    def path_helper(self, resource, operations, path=None, **kwargs) -> str:
        operations.update(yaml_utils.load_operations_from_docstring(resource.__doc__) or {})
        path = path or self.resource_uri_mapping[resource]["uri"]

        methods = self.resource_uri_mapping[resource]["methods"]

        for method_name, method_handler in methods.items():
            docstring_yaml = yaml_utils.load_yaml_from_docstring(method_handler.__doc__)
            operations[method_name] = docstring_yaml or {}
        return path

    def _generate_resource_uri_mapping(self, app: web.Application) -> dict:
        routes = app.router.routes()
        mapping = {}
        for route in routes:
            uri = self._get_uri(route)
            resource = route.handler
            mapping[resource] = {
                "uri": uri,
                "methods": {},
            }
            if issubclass_safe(resource, web.View):
                for attr in dir(resource):
                    if attr.upper() in METH_ALL:
                        mapping[resource]["methods"][attr] = getattr(resource, attr)
            else:
                method = route.method.lower()
                mapping[resource]["methods"][method] = resource

        return mapping

    def _get_uri(self, route: AbstractRoute) -> str:
        path_info = route.resource.get_info()
        return path_info.get("path") or path_info.get("formatter")
