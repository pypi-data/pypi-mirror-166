# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_limiterx']

package_data = \
{'': ['*']}

install_requires = \
['fastapi', 'redis']

setup_kwargs = {
    'name': 'fastapi-limiterx',
    'version': '0.1.6',
    'description': 'A request rate limiter for fastapi',
    'long_description': '# fastapi-limiterx\n\n[![pypi](https://img.shields.io/pypi/v/fastapi-limiter.svg?style=flat)](https://pypi.python.org/pypi/fastapi-limiter)\n[![license](https://img.shields.io/github/license/long2ice/fastapi-limiter)](https://github.com/long2ice/fastapi-limiter/blob/master/LICENCE)\n[![workflows](https://github.com/long2ice/fastapi-limiter/workflows/pypi/badge.svg)](https://github.com/long2ice/fastapi-limiter/actions?query=workflow:pypi)\n[![workflows](https://github.com/long2ice/fastapi-limiter/workflows/ci/badge.svg)](https://github.com/long2ice/fastapi-limiter/actions?query=workflow:ci)\n\n## Introduction\n\nFastAPI-Limiterx is a rate limiting tool for [fastapi](https://github.com/tiangolo/fastapi) routes with lua script.\n\n## Requirements\n\n- [redis](https://redis.io/)\n\n## Install\n\nJust install from pypi\n\n```shell script\n> pip install fastapi-limiterx\n```\n\n## Quick Start\n\nFastAPI-Limiterx is simple to use, which just provide a dependency `RateLimiter`, the following example allow `2` times\nrequest per `5` seconds in route `/`.\n\n```py\nimport aioredis\nimport uvicorn\nfrom fastapi import Depends, FastAPI\n\nfrom fastapi_limiterx import FastAPILimiter\nfrom fastapi_limiterx.depends import RateLimiter\n\napp = FastAPI()\n\n\n@app.on_event("startup")\nasync def startup():\n    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)\n    await FastAPILimiter.init(redis)\n\n\n@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])\nasync def index():\n    return {"msg": "Hello World"}\n\n\nif __name__ == "__main__":\n    uvicorn.run("main:app", debug=True, reload=True)\n```\n\n## Usage\n\nThere are some config in `FastAPILimiter.init`.\n\n### redis\n\nThe `redis` instance of `aioredis`.\n\n### prefix\n\nPrefix of redis key.\n\n### identifier\n\nIdentifier of route limit, default is `ip`, you can override it such as `userid` and so on.\n\n```py\nasync def default_identifier(request: Request):\n    forwarded = request.headers.get("X-Forwarded-For")\n    if forwarded:\n        return forwarded.split(",")[0]\n    return request.client.host + ":" + request.scope["path"]\n```\n\n### callback\n\nCallback when access is forbidden, default is raise `HTTPException` with `429` status code.\n\n```py\nasync def default_callback(request: Request, response: Response, pexpire: int):\n    """\n    default callback when too many requests\n    :param request:\n    :param pexpire: The remaining milliseconds\n    :param response:\n    :return:\n    """\n    expire = ceil(pexpire / 1000)\n\n    raise HTTPException(\n        HTTP_429_TOO_MANY_REQUESTS, "Too Many Requests", headers={"Retry-After": str(expire)}\n    )\n```\n\n## Multiple limiters\n\nYou can use multiple limiters in one route.\n\n```py\n@app.get(\n    "/multiple",\n    dependencies=[\n        Depends(RateLimiter(times=1, seconds=5)),\n        Depends(RateLimiter(times=2, seconds=15)),\n    ],\n)\nasync def multiple():\n    return {"msg": "Hello World"}\n```\n\nNot that you should note the dependencies orders, keep lower of result of `seconds/times` at the first.\n\n## Rate limiting within a websocket.\n\nWhile the above examples work with rest requests, FastAPI also allows easy usage\nof websockets, which require a slightly different approach.\n\nBecause websockets are likely to be long lived, you may want to rate limit in\nresponse to data sent over the socket.\n\nYou can do this by rate limiting within the body of the websocket handler:\n\n```py\n@app.websocket("/ws")\nasync def websocket_endpoint(websocket: WebSocket):\n    await websocket.accept()\n    ratelimit = WebSocketRateLimiter(times=1, seconds=5)\n    while True:\n        try:\n            data = await websocket.receive_text()\n            await ratelimit(websocket, context_key=data) # NB: context_key is optional\n            await websocket.send_text(f"Hello, world")\n        except WebSocketRateLimitException: # Thrown when rate limit exceeded.\n            await websocket.send_text(f"Hello again")\n```\n\n## Lua script\n\nThe lua script used.\n\n```lua\nlocal key = KEYS[1]\nlocal limit = tonumber(ARGV[1])\nlocal expire_time = ARGV[2]\n\nlocal current = tonumber(redis.call(\'get\', key) or "0")\nif current > 0 then\n    if current + 1 > limit then\n        return redis.call("PTTL", key)\n    else\n        redis.call("INCR", key)\n        return 0\n    end\nelse\n    redis.call("SET", key, 1, "px", expire_time)\n    return 0\nend\n```\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/long2ice/fastapi-limiter/blob/master/LICENCE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/fastapi-limiter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
