import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7569499427:AAFbSNvRycx1qisz0L2s6uCeJyhxxp5MeSE"
ADMIN_ID = 5885372168
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome!\nUse /get <password> to unlock today's video!")

async def set_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /set <password> <video_url>")
        return

    password, video_url = context.args
    data = load_data()
    data[password] = video_url
    save_data(data)
    await update.message.reply_text(f"✅ Video set for password `{password}`", parse_mode="Markdown")

async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /get <password>")
        return

    password = context.args[0]
    data = load_data()

    if password in data:
        await update.message.reply_text(f"🔓 Here's your video:\n{data[password]}")
    else:
        await update.message.reply_text("❌ Invalid password!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set", set_video))
    app.add_handler(CommandHandler("get", get_video))
    app.run_polling()
