import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.voice:
        await update.message.reply_voice(update.message.voice.file_id)

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, echo_voice))

app.run_polling()
