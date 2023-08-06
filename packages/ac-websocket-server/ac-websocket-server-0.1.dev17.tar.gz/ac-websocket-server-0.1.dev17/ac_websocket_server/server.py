'''Assetto Corsa Websocket Server Class'''

import asyncio
import logging
import os
import websockets

from ac_websocket_server.debug import monitor_tasks
from ac_websocket_server.constants import HOST, PORT
from ac_websocket_server.error import WebsocketsServerError
from ac_websocket_server.game import GameServer
from ac_websocket_server.grid import Grid
from ac_websocket_server.handlers import handler
from ac_websocket_server.observer import Observer
from ac_websocket_server.protocol import Protocol
from ac_websocket_server.tracker import TrackerServer

EXTRA_DEBUG = False


class WebsocketsServer(Observer):
    '''Represents an Assetto Corsa WebSocket Server.

    Allows control of an Assetto Corsa server with a websockets interface.'''
    # pylint: disable=logging-fstring-interpolation

    def __init__(self,
                 server_directory: str = None,
                 host: str = HOST,
                 port: int = PORT
                 ) -> None:

        self.__logger = logging.getLogger('ac-ws.ws-server')

        if EXTRA_DEBUG:
            asyncio.get_event_loop().create_task(monitor_tasks())

        self.connected = set()

        self.host = host
        self.port = port

        if not server_directory:
            self.server_directory = os.getcwd()
        else:
            self.server_directory = server_directory

        try:
            self.game = GameServer(server_directory=self.server_directory)
            self.game.subscribe(self)
            self.game.grid.subscribe(self)
        except WebsocketsServerError as error:
            self.__logger.error(f'Fatal error {error}')
            raise

        try:
            self.tracker = TrackerServer(self.server_directory)
            self.tracker.subscribe(self)
        except WebsocketsServerError as error:
            self.__logger.error(f'Unable to start tracker: {error}')

        self.stop_server: asyncio.Future = None

        self.__notifier_queue: asyncio.Queue = asyncio.Queue()

    async def consumer(self, message):
        '''ACWS consumer function for all received messages from client'''
        # pylint: disable=logging-fstring-interpolation, line-too-long

        if message == b'\n':
            return

        self.__logger.debug(f'Received message: {message}')

        if isinstance(message, bytes):
            message_string = str(message.strip(), 'utf-8')
        else:
            message_string = message.strip()

        message_words = message_string.split()
        message_funcs = {'grid': self.game.grid.consumer,
                         'server': self.game.consumer,
                         'shutdown': self.shutdown,
                         'tracker': self.tracker.consumer}

        if message_funcs.get(message_words[0]) and len(message_words) > 1:
            await message_funcs[message_words[0]](message_words[1:])
            return

        await self.__notifier_queue.put(Protocol.error(
            msg=f'Received unrecognised message: {message}'))

    async def handler(self, websocket):
        '''ACWS handler function for websocket connection'''

        self.connected.add(websocket)

        await websocket.send(Protocol.success(
            msg=f'Welcome to the Assetto Corsa WebSocket server running at {self.host}:{self.port}'))

        await handler(websocket, self.consumer, self.producer)

    async def notify(self, notifier):
        '''Receive a notification of a new message from
        notifier instance.  Pull the data off the notifier's
        queue and store in the local queue.'''

        message = await notifier.get()
        await self.__notifier_queue.put(message)

    async def producer(self):
        '''Pull a message off the queue and send on websocket'''
        data = await self.__notifier_queue.get()
        self.__logger.debug(f'Sending message: {data}')
        return data

    async def start(self):
        '''Start the websocket server'''

        try:

            self.__logger.info('Starting websocket server')

            self.stop_server = asyncio.Future()

            async with websockets.serve(self.handler, self.host, self.port):
                await self.stop_server

            self.__logger.info('Stopping websocket server')

        except KeyboardInterrupt:
            self.__logger.info('Interupting the server')

    async def stop(self):
        '''Stop the websocket server'''

        self.stop_server.set_result(True)

    async def shutdown(self, message: str = None):
        '''
        Shutdown the ACWS server.

        Note that running AC servers and trackers will NOT be stopped.
        '''
        await self.__notifier_queue.put(Protocol.success(
            msg=f'Shutting down the WebSocket server running at {self.host}:{self.port}'))

        self.__logger.info('Shutting down the server')
        await self.stop()
