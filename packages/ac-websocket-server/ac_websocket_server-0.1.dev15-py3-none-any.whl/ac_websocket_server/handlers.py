'''Assetto Corsa Websocket handlers'''

import asyncio


async def consumer_handler(websocket, consumer):
    '''Consumer messages from websocket and pass to user function'''
    async for message in websocket:
        await consumer(message)


async def handler(websocket, consumer, producer):
    '''Setup consumer and producer handlers.'''

    consumer_task = asyncio.create_task(consumer_handler(websocket, consumer))
    producer_task = asyncio.create_task(producer_handler(websocket, producer))
    _done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()


async def producer_handler(websocket, producer):
    '''Send user producer output to websocket'''
    # pylint: disable=broad-except
    while True:
        try:
            await websocket.send(await producer())
        except Exception as err:
            print(err)
