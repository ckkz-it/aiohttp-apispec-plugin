import pytest
from aiohttp import web
from apispec import APISpec

from aiohttp_apispec_plugin import AioHttpPlugin


@pytest.fixture()
def get_spec():
    def spec(app: web.Application):
        return APISpec(
            title="AioHttp Application",
            version="1.0.0",
            openapi_version="3.0.3",
            plugins=[
                AioHttpPlugin(app)
            ],
        )

    return spec


@pytest.fixture()
def app():
    app_ = web.Application()
    return app_


class TestPathHelpers:
    def test_get_view(self, app: web.Application, get_spec):
        class DummyView(web.View):
            async def get(self):
                """Dummy View
                ---
                description: Get Dummy Description
                responses:
                    200:
                        description: Get Response Description
                """

        expected = {
            "description": "Get Dummy Description",
            "responses": {"200": {"description": "Get Response Description"}},
        }
        app.router.add_view("/dummy", DummyView)
        spec = get_spec(app)
        spec.path(resource=DummyView)
        assert spec._paths["/dummy"]["get"] == expected

    def test_post_view(self, app: web.Application, get_spec):
        class DummyView(web.View):
            async def post(self):
                """Dummy View
                ---
                description: Post Dummy Description
                responses:
                    200:
                        description: Post Response Description
                """

        expected = {
            "description": "Post Dummy Description",
            "responses": {"200": {"description": "Post Response Description"}},
        }
        app.router.add_view("/dummy", DummyView)
        spec = get_spec(app)
        spec.path(resource=DummyView)
        assert spec._paths["/dummy"]["post"] == expected

    def test_delete_view(self, app: web.Application, get_spec):
        class DummyView(web.View):
            async def delete(self):
                """Dummy View
                ---
                description: Delete Dummy Description
                responses:
                    204:
                        description: Delete Response Description
                """

        expected = {
            "description": "Delete Dummy Description",
            "responses": {"204": {"description": "Delete Response Description"}},
        }
        app.router.add_view("/dummy", DummyView)
        spec = get_spec(app)
        spec.path(resource=DummyView)
        assert spec._paths["/dummy"]["delete"] == expected

    def test_function_handler(self, app: web.Application, get_spec):
        async def dummy_handler(request):
            """Dummy Route
            ---
            description: Route Dummy Description
            responses:
                201:
                    description: Route Response Description
            """

        expected = {
            "description": "Route Dummy Description",
            "responses": {"201": {"description": "Route Response Description"}},
        }
        app.router.add_route("POST", "/dummy", dummy_handler)
        spec = get_spec(app)
        spec.path(resource=dummy_handler)
        assert spec._paths["/dummy"]["post"] == expected
