import psutil
import asyncio
import time
import configparser
import platform
import logging

class CPUMonitor:
    def __init__(self, discord_handler, config_file):
        self.discord_handler = discord_handler
        config = configparser.ConfigParser()
        config.read(config_file)
        self.cpu_temp_limit = float(config['Discord'].get('cpu_temp_limit', 80))
        self.notification_interval = int(config['Discord'].get('cpu_temp_notification_interval', 10)) * 60
        self.last_notification_time = 0
        self.over_limit = False
        self.platform = platform.system()
        # Placeholder for future Windows implementation
        if self.platform == 'Windows':
            # CPU temperature monitoring for Windows can be implemented here in the future.
            self.cpu_temp_supported = False
            logging.info("CPU temperature monitoring is not supported on Windows.")
        else:
            self.cpu_temp_supported = True
            logging.info("CPU temperature monitoring is enabled.")

    async def start(self):
        while True:
            await self.check_cpu_temperature()
            await asyncio.sleep(5)  # Check every 5 seconds

    async def check_cpu_temperature(self):
        if not self.cpu_temp_supported:
            return  # Skip CPU temperature monitoring on unsupported platforms

        temps = psutil.sensors_temperatures()
        if not temps:
            logging.warning("No temperature sensors found.")
            return
        cpu_temps = []
        for name in temps:
            if 'cpu' in name.lower() or 'coretemp' in name.lower():
                cpu_temps.extend(temps[name])
        if not cpu_temps:
            logging.warning("No CPU temperature sensors found.")
            return
        current_temp = max([t.current for t in cpu_temps])

        if current_temp > self.cpu_temp_limit:
            now = time.time()
            if not self.over_limit or now - self.last_notification_time > self.notification_interval:
                self.over_limit = True
                self.last_notification_time = now
                message = f"CPU temperature is above limit: {current_temp:.2f}°C."
                await self.discord_handler.send_message(message)
                logging.info(f"CPU temperature exceeded limit: {current_temp:.2f}°C")
        else:
            self.over_limit = False
