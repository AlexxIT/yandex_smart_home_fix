from aiohttp.frozenlist import FrozenList
from aiohttp.web import middleware
from aiohttp.web_response import Response
from homeassistant.core import HomeAssistant


async def async_setup(hass: HomeAssistant, hass_config: dict):
    @middleware
    async def fix_middleware(request, handler):
        resp: Response = await handler(request)
        if request.raw_path == '/auth/token':
            resp._compression = False
        return resp

    hass.http.app._middlewares = FrozenList(
        list(hass.http.app.middlewares) + [fix_middleware]
    )
    hass.http.app._middlewares_handlers = tuple(
        hass.http.app._prepare_middleware()
    )
    return True
