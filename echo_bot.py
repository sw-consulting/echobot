# Copyright (c) 2025 Maxim Samsonov  All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import signal
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.voice:
        await update.message.reply_voice(update.message.voice.file_id)

# Signal handler for graceful shutdown
def signal_handler(signal_num, frame):
    print(f"Received signal {signal_num}. Shutting down...")
    asyncio.create_task(shutdown())

async def shutdown():
    """Gracefully shut down the bot application"""
    print("Stopping the bot...")
    await app.stop()
    print("Bot stopped successfully")
    # Stop the event loop
    asyncio.get_event_loop().stop()

if __name__ == "__main__":
    # Set up the bot
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, echo_voice))

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Handles Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler) # Handles termination signal

    print("Bot started. Press Ctrl+C to stop.")

    # Run the bot until it's stopped
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    print("Bot has been stopped.")
