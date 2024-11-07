import platform
import asyncio
import logging
from services_monitor import ServicesMonitor
from disk_monitor import DiskMonitor
from cpu_monitor import CPUMonitor
from shutdown_monitor import ShutdownMonitor

class EventMonitor:
    def __init__(self, discord_handler):
        self.discord_handler = discord_handler
        self.monitors = []
        system = platform.system()

        if system == 'Linux':
            self.monitors.append(ServicesMonitor(self.discord_handler, 'servicesLinux.txt'))
            self.monitors.append(ShutdownMonitor(self.discord_handler))
        elif system == 'Windows':
            self.monitors.append(ServicesMonitor(self.discord_handler, 'servicesWindows.txt'))
            self.monitors.append(ShutdownMonitor(self.discord_handler))
        else:
            logging.error(f"Unsupported platform: {system}")
            raise Exception(f"Unsupported platform: {system}")

        self.monitors.append(DiskMonitor(self.discord_handler))
        self.monitors.append(CPUMonitor(self.discord_handler, 'config.txt'))

    async def start_monitoring(self):
        logging.info("Starting monitoring tasks.")
        tasks = [asyncio.create_task(monitor.start()) for monitor in self.monitors]
        await asyncio.gather(*tasks)
