async def __aenter__(self):
    return await self


async def __aexit__(self, exc_type, exc_value, traceback):
    self.ws_server.close()
    await self.ws_server.wait_closed()


async def __await_impl__(self):
    # Duplicated with __iter__ because __await__ must call coroutines with
    # await in Python 3.7 while __iter__ must call them with yield from to
    # preserve compatibility with Python 3.4.
    server = await self._creating_server
    self.ws_server.wrap(server)
    return self.ws_server


def __await__(self):
    # I'm not finding a better way to take advantage of PEP 492.
    return __await_impl__(self).__await__()
