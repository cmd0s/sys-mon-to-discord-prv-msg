import configparser
import platform
import discord
import asyncio
from datetime import datetime, timezone
import logging

from event_monitor import EventMonitor

class DiscordHandler:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.txt')
        self.bot_token = config['Discord']['bot_token']
        self.user_id = int(config['Discord']['user_id'])
        self.hostname = platform.node()
        intents = discord.Intents.default()
        intents.message_content = True  # Required for direct messages in some cases
        self.client = discord.Client(intents=intents)
        self.event_monitor = None
        self.user = None

    def run_bot(self):
        @self.client.event
        async def on_ready():
            logging.info(f'Logged in as {self.client.user}')
            try:
                self.user = await self.client.fetch_user(self.user_id)
                # Send startup notification
                await self.send_message("Monitoring application has started.")
                self.event_monitor = EventMonitor(self)
                # Start monitoring tasks
                await self.event_monitor.start_monitoring()
            except Exception as e:
                logging.error(f"Error in on_ready: {e}")

        self.client.run(self.bot_token)

    def get_utc_timestamp(self):
        utc_now = datetime.now(timezone.utc)
        formatted_time = utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')
        return formatted_time

    async def send_message(self, message):
        timestamp = self.get_utc_timestamp()
        formatted_message = f"{timestamp}\n**[{self.hostname}]** {message}"
        if self.user:
            try:
                await self.user.send(formatted_message)
                logging.info(f"Sent message to user: {message}")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
        else:
            logging.warning("User not found; cannot send message.")
