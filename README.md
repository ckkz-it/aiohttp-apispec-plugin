# aiohttp-apispec-plugin

[apispec](https://github.com/marshmallow-code/apispec) plugin that generates OpenAPI specification  for [aiohttp](https://docs.aiohttp.org/en/stable/) web applications.


## Installation

```bash
pip install aiohttp-apispec-plugin
```

## Examples

Consider we have the following sqlalchemy tables (models):

```python
from aiohttp import web
from aiohttp_apispec_plugin import AioHttpPlugin
from apispec import APISpec

class UserView(web.View):
    async def get(self):
        """User Detail View
        ---
        summary: Get User
        description: Get User Data
        parameters:
            - name: user_id
            in: path
            description: User ID
            required: true
            schema:
              type: string
        responses:
            200:
                description: Successfully retrieved user details
                content:
                    application/json:
                        schema:
                            properties:
                                id:
                                    type: integer
                                username:
                                    type: string
                                first_name:
                                    type: string
                                last_name:
                                    type: string
        """

app = web.Application()
app.router.add_view("/api/v1/users/{user_id}", UserView)

# Create an APISpec
spec = APISpec(
    title="AioHttp Application",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[
        AioHttpPlugin(app),
    ],
)

spec.path(view=UserView)
```

## Requirements

Python >= 3.6

#### Dependencies:
- aiohttp
- apispec
