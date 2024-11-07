import psutil
import asyncio
import platform
import subprocess
import logging

class ServicesMonitor:
    def __init__(self, discord_handler, services_file):
        self.discord_handler = discord_handler
        self.services_file = services_file
        self.services = {}
        self.load_services()
        self.platform = platform.system()

    def load_services(self):
        try:
            with open(self.services_file, 'r') as f:
                for line in f:
                    service_name = line.strip()
                    if service_name:
                        self.services[service_name] = None  # Initialize with None status
            logging.info(f"Loaded services from {self.services_file}")
        except FileNotFoundError:
            logging.error(f"Services file not found: {self.services_file}")

    async def start(self):
        while True:
            await self.check_services()
            await asyncio.sleep(5)  # Check every 5 seconds

    async def check_services(self):
        for service_name in self.services:
            try:
                if self.platform == 'Windows':
                    service = psutil.win_service_get(service_name)
                    status = service.status()
                elif self.platform == 'Linux':
                    status = await self.get_linux_service_status(service_name)
                else:
                    status = 'unknown'

                if self.services[service_name] != status:
                    self.services[service_name] = status
                    message = f"Service '{service_name}' changed status to **{status}**."
                    await self.discord_handler.send_message(message)
                    logging.info(f"Service '{service_name}' status changed to {status}")
            except Exception as e:
                logging.error(f"Error checking service {service_name}: {e}")

    async def get_linux_service_status(self, service_name):
        try:
            proc = await asyncio.create_subprocess_exec(
                'systemctl', 'is-active', service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            output = stdout.decode().strip()
            return output
        except Exception as e:
            logging.error(f"Error getting status for service {service_name}: {e}")
            return 'inactive'
