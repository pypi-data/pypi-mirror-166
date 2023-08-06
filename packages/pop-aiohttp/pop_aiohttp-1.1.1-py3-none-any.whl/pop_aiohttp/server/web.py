from aiohttp import web


async def text_response(hub, text):
    """
    Return a text response
    """
    return web.Response(text=text)


async def json_response(hub, data):
    """
    Return a JSON response
    """
    return web.json_response(data)


async def response_handler(hub, response):
    """
    Handle responses without being explicit about return data type.
    """
    if isinstance(response, str):
        ret = await hub.server.web.text_response(response)
    else:
        ret = await hub.server.web.json_response(response)
    return ret


async def init(hub, routes=None):
    """
    Create a simple aiohttp application and allow routes to be passed.

    Expected format for incoming routes is a list of routes that are lists
    themselves of 'verb', 'location', and request handler function.

    ..code-block::

        routes = [
            ["get", "/foo", hub.something.get_foo],
            ["post", "/bar", hub.something.post_bar],
            ["/baz", hub.something.get_baz],  # defaults to 'get'
            [hub.something.get_default],  # defaults to 'get' and '/'
        ]

    """
    app = web.Application()
    try:
        for idx, route in enumerate(routes):
            if len(route) > 3 or len(route) < 1:
                hub.log.warning(f"Malformed route definition: {route}")
                continue
            if len(route) == 1:
                route.insert(0, "/")
            if len(route) == 2:
                route.insert(0, "get")
            route = getattr(web, route[0])(route[1], route[2])
            routes[idx] = route
        app.add_routes(routes)
    except TypeError as exc:
        hub.log.error(exc)
    return app


def run(hub, routes=None, **kwargs):
    """
    Start a simple aiohttp web server and allow routes to be passed.
    """
    app = hub.server.web.init(routes)
    try:
        web.run_app(app, **kwargs)
    finally:
        raise web.GracefulExit()
