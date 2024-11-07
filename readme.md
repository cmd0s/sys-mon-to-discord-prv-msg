
# System Monitoring to Discord Private Messages

## Overview

**System Monitoring to Discord Private Messages** is a Python 3 application that monitors specific system events and sends direct messages to a specified Discord user when these events occur. The application is designed to run on both **Ubuntu Server 24.04** and **Windows 10/11**, utilizing a virtual environment (`venv`) for Python dependencies.

### Features

- **Service Status Monitoring**: Monitors the status of specified system services and sends a notification if their status changes.
- **Disk Usage Monitoring**: Monitors specified disk paths and sends a notification when disk usage exceeds a defined limit.
- **CPU Temperature Monitoring**: Monitors the CPU temperature and sends a notification if it exceeds a defined threshold (**Linux only**).
- **Shutdown and Restart Monitoring**: Detects system shutdown or restart events and sends a notification (**Linux only**).
- **Logging**: Logs events and errors to both the console and a file (`application.log`) for better traceability.
- **Cross-Platform Support**: Automatically detects the operating system and loads the appropriate configurations and libraries.
- **Discord Integration**: Sends direct messages to a specified Discord user using a Discord bot.

## Project Structure

```
.
├── main.py
├── discord_handler.py
├── event_monitor.py
├── services_monitor.py
├── disk_monitor.py
├── cpu_monitor.py
├── shutdown_monitor.py
├── config.txt
├── servicesLinux.txt
├── servicesWindows.txt
├── drivesLinux.txt
├── drivesWindows.txt
├── requirements.txt
├── application.log
└── README.md
```

### File Descriptions

- **main.py**: The entry point of the application. Initializes the logging system and the Discord handler, and starts the bot.
- **discord_handler.py**: Handles interactions with Discord, including sending messages and managing the bot client.
- **event_monitor.py**: Manages the initialization and coordination of various monitoring tasks.
- **services_monitor.py**: Monitors the status of specified system services.
- **disk_monitor.py**: Monitors disk usage of specified paths.
- **cpu_monitor.py**: Monitors CPU temperature and sends notifications when thresholds are exceeded (**Linux only**).
- **shutdown_monitor.py**: Monitors for system shutdown or restart events (**Linux only**).
- **config.txt**: Configuration file containing Discord bot settings and monitoring thresholds.
- **servicesLinux.txt**: List of services to monitor on Linux.
- **servicesWindows.txt**: List of services to monitor on Windows.
- **drivesLinux.txt**: List of disk paths and usage limits to monitor on Linux.
- **drivesWindows.txt**: List of disk paths and usage limits to monitor on Windows.
- **requirements.txt**: Lists all Python dependencies required to run the application.
- **application.log**: The log file where all events and errors are recorded.
- **README.md**: Documentation and instructions for the application.

## Configuration Files

### config.txt

This file contains configuration settings for the Discord bot and CPU temperature monitoring.

```ini
[Discord]
bot_token = YOUR_DISCORD_BOT_TOKEN
user_id = YOUR_DISCORD_USER_ID
cpu_temp_limit = 80  # Maximum allowed CPU temperature in degrees Celsius
cpu_temp_notification_interval = 10  # Notification interval in minutes
```

- **bot_token**: The token for your Discord bot. Replace `YOUR_DISCORD_BOT_TOKEN` with your actual bot token.
- **user_id**: The Discord ID of the user to whom the bot will send direct messages.
- **cpu_temp_limit**: The CPU temperature threshold for sending notifications (**Linux only**).
- **cpu_temp_notification_interval**: The minimum interval between CPU temperature notifications, in minutes.

### servicesLinux.txt

List of system services to monitor on **Linux**. Each line contains the name of a service.

Example:

```
w3p_bsh.service
w3p_geth.service
```

### servicesWindows.txt

List of system services to monitor on **Windows**. Each line contains the name of a service.

Example:

```
TeamViewer
```

### drivesLinux.txt

List of disk paths and usage limits to monitor on **Linux**. Each line contains a path and a usage limit percentage.

Example:

```
/dev/sda1 90
/mnt/storage 80
/home/ethereum 95
```

### drivesWindows.txt

List of disk paths and usage limits to monitor on **Windows**. Each line contains a path and a usage limit percentage.

Example:

```
C:/ 90
D:/ 80
```

## Installation and Setup

### Prerequisites

- **Python 3.x** installed on your system.
- **Administrator or root permissions** may be required for certain monitoring features.
- **Linux**: `lm-sensors` package for CPU temperature monitoring.

### Steps for Both Linux and Windows

1. **Clone the Repository**

   ```bash
   git clone https://github.com/cmd0s/sys-mon-to-discord-prv-msg.git
   cd sys-mon-to-discord-prv-msg
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Linux:**

     ```bash
     source venv/bin/activate
     ```

   - **Windows:**

     ```cmd
     venv\Scripts\activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the Application**

   - **Edit `config.txt`**

     Replace placeholders with your actual Discord bot token and user ID.

     ```ini
     [Discord]
     bot_token = YOUR_DISCORD_BOT_TOKEN
     user_id = YOUR_DISCORD_USER_ID
     cpu_temp_limit = 80
     cpu_temp_notification_interval = 10
     ```

   - **Edit `servicesLinux.txt` or `servicesWindows.txt`**

     List the services you want to monitor.

   - **Edit `drivesLinux.txt` or `drivesWindows.txt`**

     List the disk paths and usage limits you want to monitor.

6. **Additional Setup for Linux**

   - Install `lm-sensors` for CPU temperature monitoring.

     ```bash
     sudo apt-get install lm-sensors
     sudo sensors-detect
     ```

7. **Run the Application**

   ```bash
   python main.py
   ```

   - The application will start monitoring and send notifications as configured.
   - Log messages will be displayed in the console and saved to `application.log`.

## Discord Bot Setup

Sending direct messages to a user on Discord requires setting up a Discord bot, obtaining a bot token, and knowing the user's Discord ID. The bot must share a server with the user or the user must have sent a direct message to the bot at least once.

### Creating a Discord Bot

1. **Go to the Discord Developer Portal**

   Visit the [Discord Developer Portal](https://discord.com/developers/applications).

2. **Create a New Application**

   - Click on **"New Application"**.
   - Enter a name for your application and click **"Create"**.

3. **Add a Bot to Your Application**

   - Navigate to the **"Bot"** tab on the left sidebar.
   - Click on **"Add Bot"** and confirm by clicking **"Yes, do it!"**.

4. **Enable "Message Content Intent"**

   - Under the **"Privileged Gateway Intents"** section, enable the **"Message Content Intent"**.
   - This is necessary for the bot to read message content and send direct messages properly.

5. **Retrieve the Bot Token**

   - Under the **"Bot"** tab, click on **"Copy"** under **"Token"**.
   - **Keep this token secure** and do not share it publicly.

### Inviting the Bot to Your Server

1. **Navigate to OAuth2 URL Generator**

   - Go to the **"OAuth2"** tab.
   - Click on **"URL Generator"**.

2. **Generate an Invite Link**

   - Under **"Scopes"**, select **"bot"**.
   - Under **"Bot Permissions"**, select **"Send Messages"**.
   - Copy the generated URL.

3. **Invite the Bot**

   - Paste the URL into your browser.
   - Select the server you want to add the bot to and authorize it.

### Obtaining Your Discord User ID

You need your Discord User ID to configure the application.

1. **Enable Developer Mode**

   - Open Discord.
   - Go to **User Settings** > **Advanced**.
   - Enable **Developer Mode**.

2. **Copy Your User ID**

   - Right-click on your username in Discord.
   - Click **"Copy ID"**.

For more detailed instructions, refer to [this guide](https://support.playhive.com/discord-user-id/).

### Sending Direct Messages

- **Requirement**: The bot must share a server with you or you must have sent a direct message to the bot at least once.
- **Establishing a DM Channel**: Send a direct message to your bot to establish the DM channel.

## Application Details

### How It Works

1. **Startup Notification**

   - When the application starts, it sends a direct message to the specified Discord user indicating that monitoring has begun.

2. **Service Monitoring**

   - The application monitors the status of services listed in `servicesLinux.txt` or `servicesWindows.txt`.
   - If a service changes status (e.g., from "running" to "stopped"), a notification is sent.

3. **Disk Usage Monitoring**

   - Monitors disk usage for paths specified in `drivesLinux.txt` or `drivesWindows.txt`.
   - Sends a notification when disk usage exceeds the specified limit.
   - Notifications are sent only once when crossing the threshold to avoid spamming.

4. **CPU Temperature Monitoring**

   - Monitors CPU temperature on **Linux** systems.
   - Sends a notification when the temperature exceeds the specified limit.
   - Notifications are throttled based on `cpu_temp_notification_interval`.

5. **Shutdown and Restart Monitoring**

   - On **Linux** systems, the application listens for shutdown and restart signals (`SIGTERM` and `SIGINT`).
   - Sends a notification when such an event is detected.

6. **Logging**

   - The application logs events and errors to both the console and a log file named `application.log`.
   - Logs include timestamps, severity levels, and informative messages.
   - This aids in debugging and provides a record of the application's activities.

### Logging Configuration

- **Log File**: `application.log`
- **Log Levels**: `INFO`, `WARNING`, `ERROR`
- **Console Output**: Log messages are also displayed in the console.
- **Customization**:

  - The logging configuration is set up in `main.py`.
  - You can adjust logging levels and formats as needed.
  - By default, both console and file handlers are set to `INFO` level.

#### Adjusting Logging Levels

You can adjust the logging levels for the console and file outputs independently in `main.py`:

```python
# Set levels for handlers
c_handler.setLevel(logging.INFO)  # Console handler level
f_handler.setLevel(logging.DEBUG)  # File handler level
```

#### Log Rotation (Optional)

To prevent the log file from growing indefinitely, you can implement log rotation using `RotatingFileHandler`:

```python
from logging.handlers import RotatingFileHandler

f_handler = RotatingFileHandler('application.log', maxBytes=1048576, backupCount=5)
```

- **maxBytes**: Maximum size of the log file before rotation (e.g., 1 MB).
- **backupCount**: Number of backup files to keep.

### Tips and Tricks

- **Running on Startup**

  - **Linux**: Use `systemd` to create a service that runs the application at startup.
  - **Windows**: Use Task Scheduler to run the application at startup.

- **Logging**

  - Review the `application.log` file regularly to monitor the application's behavior.
  - Adjust the logging level in `main.py` if you want more or less verbosity.
  - Both console and file outputs help in real-time monitoring and historical analysis.

- **Security**

  - Keep your Discord bot token and user ID secure. Do not share them publicly or commit them to a public repository.

- **Testing**

  - Test each monitoring feature individually to ensure it works as expected.
  - Use low thresholds temporarily to trigger notifications during testing.

- **Extensibility**

  - The modular design allows for easy addition of new monitoring features.
  - You can create additional monitoring modules and integrate them into `event_monitor.py`.

## Troubleshooting

- **Permissions**

  - Ensure the application has sufficient permissions to monitor services and system metrics.
  - You may need to run the application with elevated privileges.

- **Dependencies**

  - Make sure all dependencies are installed in your virtual environment.
  - If you encounter issues, try reinstalling dependencies with:

    ```bash
    pip install --upgrade --force-reinstall -r requirements.txt
    ```

- **CPU Temperature Monitoring on Windows**

  - Currently, CPU temperature monitoring is disabled on Windows.
  - The code includes placeholders for future implementation.

- **Error Messages**

  - Monitor the console output and `application.log` for error messages.
  - Common issues include incorrect file paths or missing configuration settings.

- **Duplicate Logs**

  - If you see duplicate log entries, ensure that logging is configured correctly in `main.py`, and `logging.basicConfig` is not called elsewhere.

- **No Console Output**

  - If log messages are not appearing in the console, verify that the `StreamHandler` is correctly configured and added to the logger in `main.py`.

## Conclusion

This application provides a flexible and extensible solution for system monitoring with notifications via Discord direct messages. The addition of logging enhances traceability and aids in debugging. By following the installation and configuration steps, including enabling the **"Message Content Intent"** in your Discord bot settings, you can tailor the monitoring to your specific needs and ensure that you're promptly notified of critical system events.

## License

This project is licensed under the GPL-3.0 license.
