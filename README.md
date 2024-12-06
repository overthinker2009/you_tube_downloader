
# Video Downloader Telegram Bot

This project is a Telegram bot that enables users to download videos from YouTube and other direct video URLs. Users must register with their phone number to access the bot's features. The project is designed for educational purposes and demonstrates the integration of Telegram's Bot API with Python.

---

## Features

- **User Registration**: Requires users to share their phone numbers for registration.
- **YouTube Video Downloads**: Downloads videos from YouTube using `yt_dlp`.
- **Direct Video URL Downloads**: Supports downloading videos from direct `.mp4` links.
- **Error Handling**: Manages errors for invalid URLs, download issues, and file size limits.
- **Database Support**: Stores registered users in a SQLite database.

---

## Prerequisites

Before running the bot, make sure you have:
1. **virtual enviroment (venv)** 
1. **Python 3.8 or higher**
2. **Telegram Bot Token**: Obtain one from [BotFather](https://core.telegram.org/bots#botfather).
3. **Required Python libraries**:
   - `pyTelegramBotAPI`
   - `yt-dlp`
   - `requests`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/video-downloader-bot.git
   cd video-downloader-bot
   ```

2. Install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your bot token:
   Open the `bot.py` file and replace the placeholder token with your actual Telegram bot token:
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN"
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

---

## Usage

1. **Start the Bot**: Send `/start` to the bot in Telegram.
2. **Register**: Tap the "Share Contact" button to register by sharing your phone number.
3. **Download Videos**:
   - Send a YouTube video URL or a direct video file URL to the bot.
   - The bot will process the request and send the downloaded video if it’s within the 50MB size limit.

---

## File Structure

- `bot.py`: Main script for the Telegram bot.
- `requirements.txt`: Python dependencies for the project.
- `bot_users.db`: SQLite database for storing user information (automatically created).
- `bot_errors.log`: Log file for errors and debugging (automatically created) information.

---

## Dependencies

Install the following libraries using `pip`:
```bash
pip install pyTelegramBotAPI yt-dlp requests
```

---

## Limitations

- **File Size**: Videos larger than 50MB cannot be sent via Telegram.
- **Supported Formats**: Currently supports `.mp4` video format for YouTube downloads.

---

## Logging and Error Handling

- Errors are logged in `bot_errors.log` for troubleshooting.
- Common errors handled include:
  - Invalid video URLs
  - Network issues
  - Exceeding Telegram’s file size limit

---

## License

This project is provided for **educational purposes only**. Feel free to modify or enhance it for personal use.

---

## Contributions

Contributions are welcome! If you have suggestions or encounter any issues, feel free to submit a pull request or create an issue.

Telegram Number: +998 (99) 767 71 17 (recomended)
Telegram Nickname: @Overthinker2009 
---

## Disclaimer

Downloading videos may be subject to copyright laws. Use this bot responsibly. Creator is not responible for actions you will take
This Bot created with this repository **https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp**