# aiohttp-apispec-plugin

[![PyPI](https://img.shields.io/pypi/v/aiohttp-apispec-plugin.svg)](https://pypi.org/project/aiohttp-apispec-plugin/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lightweight [apispec](https://github.com/marshmallow-code/apispec) plugin that generates OpenAPI specification  for [aiohttp](https://docs.aiohttp.org/en/stable/) web applications.


## Installation

```bash
pip install aiohttp-apispec-plugin
```

## Examples

#### With class based view

```python
from aiohttp import web
from aiohttp_apispec_plugin import AioHttpPlugin
from apispec import APISpec

class UserView(web.View):
    async def get(self) -> web.Response:
        """User Detail View
        ---
        summary: Get User
        description: Get User Data For Given `user_id`
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

spec.path(resource=UserView)
print(spec.to_yaml())
"""
info:
  title: AioHttp Application
  version: 1.0.0
openapi: 3.0.3
paths:
  /api/v1/users/{user_id}:
    get:
      description: Get User Data For Given `user_id`
      parameters:
      - description: User ID
        in: path
        name: user_id
        required: true
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                properties:
                  first_name:
                    type: string
                  id:
                    type: integer
                  last_name:
                    type: string
                  username:
                    type: string
          description: Successfully retrieved user details
      summary: Get User
"""
```

#### With function based view

```python
from aiohttp import web
from aiohttp_apispec_plugin import AioHttpPlugin
from apispec import APISpec

async def get_user(request: web.Request) -> web.Response:
    """User Detail View
    ---
    summary: Get User
    description: Get User Data For Given `user_id`
    responses:
      200:
        description: Successfully retrieved user details
    """

app = web.Application()
app.router.add_get("/api/v1/users/{user_id}", get_user)

# Create an APISpec
spec = APISpec(
    title="AioHttp Application",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[
        AioHttpPlugin(app),
    ],
)

spec.path(resource=get_user)
print(spec.to_yaml())  # same behavior
```

#### With [dataclasses](https://github.com/s-knibbs/dataclasses-jsonschema) plugin

```python
from dataclasses import dataclass
from aiohttp import web
from aiohttp_apispec_plugin import AioHttpPlugin
from apispec import APISpec
from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses_jsonschema.apispec import DataclassesPlugin

@dataclass
class User(JsonSchemaMixin):
    """User Schema"""
    id: int
    username: str

async def get_user(request: web.Request) -> web.Response:
    """User Detail View
    ---
    summary: Get User
    description: Get User Data For Given `user_id`
    responses:
      200:
        description: Successfully retrieved user details
        content:
            application/json:
                schema: User
    """

app = web.Application()
app.router.add_get("/api/v1/users/{user_id}", get_user)

spec = APISpec(
    title="AioHttp Application",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[
        AioHttpPlugin(app),
        DataclassesPlugin(),
    ],
)

spec.components.schema("User", schema=User)
spec.path(resource=get_user)

print(spec.to_yaml())
"""
components:
  schemas:
    User:
      description: User Schema
      properties:
        id:
          type: integer
        username:
          type: string
      required:
      - id
      - username
      type: object
info:
  title: AioHttp Application
  version: 1.0.0
openapi: 3.0.3
paths:
  /api/v1/users/{user_id}:
    get:
      description: Get User Data For Given `user_id`
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
          description: Successfully retrieved user details
      summary: Get User
"""
```

## Requirements

Python >= 3.6

#### Dependencies:
- [aiohttp](https://github.com/aio-libs/aiohttp)
- [apispec](https://github.com/marshmallow-code/apispec)
- [PyYAML](https://github.com/yaml/pyyaml)


## Other libs to check
- [aiohttp-apispec](https://github.com/maximdanilchenko/aiohttp-apispec)
- [falcon-apispec](https://github.com/alysivji/falcon-apispec)
- [dataclasses-jsonschema](https://github.com/s-knibbs/dataclasses-jsonschema)
