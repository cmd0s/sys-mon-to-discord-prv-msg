import asyncio
import platform
import signal
import logging

class ShutdownMonitor:
    def __init__(self, discord_handler):
        self.discord_handler = discord_handler
        self.platform = platform.system()

    async def start(self):
        if self.platform == 'Linux':
            loop = asyncio.get_event_loop()
            loop.add_signal_handler(signal.SIGTERM, self.handle_shutdown)
            loop.add_signal_handler(signal.SIGINT, self.handle_shutdown)
            logging.info("Shutdown monitor is running.")
            # Keep the coroutine running
            await asyncio.Future()
        elif self.platform == 'Windows':
            # Windows shutdown monitoring requires additional implementation
            logging.info("Shutdown monitoring is not implemented on Windows.")
        else:
            logging.error(f"Unsupported platform: {self.platform}")
            raise Exception(f"Unsupported platform: {self.platform}")

    def handle_shutdown(self):
        message = "System is shutting down or restarting."
        asyncio.create_task(self.discord_handler.send_message(message))
        logging.info("Shutdown or restart detected.")
