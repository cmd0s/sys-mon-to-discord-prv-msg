import asyncio
import platform
import signal
import logging

class ShutdownMonitor:
    def __init__(self, discord_handler):
        self.discord_handler = discord_handler
        self.platform = platform.system()
        self.loop = asyncio.get_event_loop()

    async def start(self):
        if self.platform == 'Linux':
            # Handle SIGTERM (system shutdown) and SIGINT (Ctrl+C)
            self.loop.add_signal_handler(signal.SIGTERM, self.handle_shutdown)
            self.loop.add_signal_handler(signal.SIGINT, self.handle_shutdown)
            logging.info("Shutdown monitor is running.")
            # Keep the coroutine running
            await asyncio.Future()
        elif self.platform == 'Windows':
            # For Ctrl+C handling on Windows
            import threading

            def windows_ctrl_c_handler():
                import msvcrt
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key == b'\x03':  # Ctrl+C
                            self.loop.call_soon_threadsafe(self.handle_shutdown)
                            break

            threading.Thread(target=windows_ctrl_c_handler, daemon=True).start()
            logging.info("Shutdown monitor is running (Windows Ctrl+C handler).")
            # Keep the coroutine running
            await asyncio.Future()
        else:
            logging.error(f"Unsupported platform: {self.platform}")
            raise Exception(f"Unsupported platform: {self.platform}")

    def handle_shutdown(self):
        logging.info("Shutdown detected.")
        asyncio.create_task(self.shutdown_sequence())

    async def shutdown_sequence(self):
        message = "Application is shutting down."
        await self.discord_handler.send_message(message)
        # Close the Discord client gracefully
        await self.discord_handler.client.close()
