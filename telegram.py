import telebot
import requests
import os
import yt_dlp
import time
import logging
import sqlite3

# Bot token
BOT_TOKEN = "8199732359:AAGsY00bsIIVnIRZrPL5FIHT2Dte934XNEc"  # Replace with your actual bot token
bot = telebot.TeleBot(BOT_TOKEN)

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    filename="bot_errors.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Database setup
DB_FILE = "bot_users.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Create table for user data
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE,
    phone_number TEXT,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton(text="Share Contact", request_contact=True)
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "Welcome! Please register by sharing your phone number. Tap the button below to proceed.",
        reply_markup=markup
    )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if not message.contact:
        bot.reply_to(message, "Error: Unable to retrieve contact information.")
        return

    phone_number = message.contact.phone_number
    chat_id = message.chat.id

    # Save to the database
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO users (chat_id, phone_number) VALUES (?, ?)",
            (chat_id, phone_number)
        )
        conn.commit()

        bot.reply_to(message, "Thank you for registering! You can now use the bot to download videos.")
    except Exception as e:
        logging.error(f"Database error: {e}", exc_info=True)
        bot.reply_to(message, "An error occurred during registration. Please try again later.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the user is registered
    cursor.execute("SELECT phone_number FROM users WHERE chat_id = ?", (message.chat.id,))
    user = cursor.fetchone()

    if not user:
        bot.reply_to(message, "You must register first by sharing your phone number. Use /start to begin.")
        return

    video_url = message.text.strip()

    if not video_url.startswith("http"):
        bot.reply_to(message, "Please send a valid video URL.")
        return

    bot.reply_to(message, "Downloading your video... Please wait!")
    try:
        video_file_path = None

        if "youtube.com" in video_url or "youtu.be" in video_url:
            bot.reply_to(message, "Downloading from YouTube...")

            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'downloaded_video.%(ext)s',
                'quiet': True,
                'noplaylist': True,
                'merge_output_format': 'mp4',
                'retries': 5,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            video_file_path = "downloaded_video.mp4"

        else:
            response = requests.head(video_url, allow_redirects=True, timeout=10)
            if response.status_code != 200:
                bot.reply_to(message, f"Error: Unable to fetch video (HTTP {response.status_code}).")
                return

            content_type = response.headers.get('Content-Type', '')
            if 'video' not in content_type:
                bot.reply_to(message, "The provided URL does not appear to be a valid video.")
                return

            video_response = requests.get(video_url, stream=True, timeout=30)
            video_response.raise_for_status()

            video_file_path = "downloaded_video.mp4"
            with open(video_file_path, 'wb') as video_file:
                for chunk in video_response.iter_content(chunk_size=1024):
                    video_file.write(chunk)

        if os.path.exists(video_file_path):
            file_size = os.path.getsize(video_file_path)
            if file_size > 50 * 1024 * 1024:
                bot.reply_to(message, "The downloaded video exceeds the 50 MB limit for Telegram bots.")
            else:
                with open(video_file_path, 'rb') as video_file:
                    bot.send_video(message.chat.id, video_file)
        else:
            bot.reply_to(message, "Error: Video file was not created.")

    except yt_dlp.utils.DownloadError as e:
        bot.reply_to(message, f"Error downloading YouTube video: {e}")
        logging.error(f"yt_dlp error: {e}", exc_info=True)
    except requests.exceptions.Timeout:
        bot.reply_to(message, "Error: The video download timed out.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Error: Could not download the video. {e}")
        logging.error(f"Request exception: {e}", exc_info=True)
    except Exception as e:
        bot.reply_to(message, f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        if video_file_path and os.path.exists(video_file_path):
            os.remove(video_file_path)


# Polling loop
while True:
    try:
        print("Bot is running...")
        bot.polling(non_stop=True)
    except Exception as e:
        logging.error(f"Polling error: {e}", exc_info=True)
        print(f"Bot polling error: {e}")
        time.sleep(15)
