import psutil
import asyncio
import platform
import logging

class DiskMonitor:
    def __init__(self, discord_handler):
        self.discord_handler = discord_handler
        self.platform = platform.system()
        self.drives_file = self.get_drives_file()
        self.drives = {}
        self.previous_states = {}
        self.load_drives()

    def get_drives_file(self):
        if self.platform == 'Linux':
            return 'drivesLinux.txt'
        elif self.platform == 'Windows':
            return 'drivesWindows.txt'
        else:
            logging.error(f"Unsupported platform: {self.platform}")
            raise Exception(f"Unsupported platform: {self.platform}")

    def load_drives(self):
        try:
            with open(self.drives_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        path, limit = parts
                        self.drives[path] = int(limit)
                        self.previous_states[path] = False
                    else:
                        logging.warning(f"Invalid line in {self.drives_file}: '{line.strip()}'")
            logging.info(f"Loaded drives from {self.drives_file}")
        except FileNotFoundError:
            logging.error(f"Drives file not found: {self.drives_file}")

    async def start(self):
        while True:
            await self.check_drives()
            await asyncio.sleep(60)  # Check every minute

    async def check_drives(self):
        for path, limit in self.drives.items():
            try:
                usage = psutil.disk_usage(path)
                percent_used = usage.percent
                over_limit = percent_used > limit
                if over_limit and not self.previous_states[path]:
                    self.previous_states[path] = True
                    message = f"Disk usage on '{path}' is above {limit}% ({percent_used:.2f}%)."
                    await self.discord_handler.send_message(message)
                    logging.info(f"Disk usage on '{path}' exceeded limit ({percent_used:.2f}% used)")
                elif not over_limit and self.previous_states[path]:
                    self.previous_states[path] = False
            except Exception as e:
                logging.error(f"Error checking disk {path}: {e}")
