async def __aenter__(self):
    return await self


async def __aexit__(self, exc_type, exc_value, traceback):
    await self.ws_client.close()


async def __await_impl__(self):
    # Duplicated with __iter__ because __await__ must call coroutines with
    # await in Python 3.7 while __iter__ must call them with yield from to
    # preserve compatibility with Python 3.4.
    transport, protocol = await self._creating_connection

    try:
        await protocol.handshake(
            self._wsuri, origin=self._origin,
            available_extensions=protocol.available_extensions,
            available_subprotocols=protocol.available_subprotocols,
            extra_headers=protocol.extra_headers,
        )
    except Exception:
        await protocol.fail_connection()
        raise

    self.ws_client = protocol
    return protocol


def __await__(self):
    # I'm not finding a better way to take advantage of PEP 492.
    return __await_impl__(self).__await__()
