"""Unmapped product starter: a Telegram bot that answers questions from your adapted data.

1. In Telegram, message @BotFather, send /newbot, and copy the token it gives you.
2. Save the token in an environment variable called TELEGRAM_BOT_TOKEN. Never paste it into this file.
     macOS or Linux:  export TELEGRAM_BOT_TOKEN="your-token"
     Windows:         set TELEGRAM_BOT_TOKEN=your-token
3. pip install -r requirements.txt, then python bot.py, and send your bot a message.
The bot runs while this program runs. To keep it online, run it on a server or a free hosting service.
"""
import os
from pathlib import Path

from lookup import describe_row, load_table, search

# Change these settings, and replace data.csv with your adapted dataset.
BOT_NAME = "Clinic Finder"
WELCOME = "Send me a town, a name or a service and I'll find matching places in our data."
DATA_FILE = Path(__file__).parent / "data.csv"
MAX_RESULTS = 3

TABLE = load_table(DATA_FILE)


def answer(query: str) -> str:
    """The reply for one message: the first few matching rows, or a hint when nothing matches."""
    rows = search(TABLE, query)
    if rows.empty:
        return "Nothing matched. Try one word, like a town or a service."
    replies = [describe_row(row) for _, row in rows.head(MAX_RESULTS).iterrows()]
    extra = len(rows) - MAX_RESULTS
    more = f"\n\n{extra} more matched. Add a word to narrow it down." if extra > 0 else ""
    return "\n\n".join(replies) + more


async def start(update, context):
    await update.message.reply_text(f"{BOT_NAME}\n{WELCOME}")


async def reply(update, context):
    await update.message.reply_text(answer(update.message.text))


def main():
    from telegram.ext import Application, CommandHandler, MessageHandler, filters

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN first. The steps are at the top of bot.py.")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler(["start", "help"], start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print(f"{BOT_NAME} is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
