import os
import logging
import pandas as pd
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("BOT_TOKEN")

EXCEL_FILE = "results.xlsx"

try:
    df = pd.read_csv("results.csv", dtype=str)
    df.fillna("", inplace=True)

    df["seating_no"] = df["seating_no"].astype(str).str.strip()
    df["arabic_name"] = df["arabic_name"].astype(str).str.strip()
    df["total_degree"] = df["total_degree"].astype(str).str.strip()

except Exception as e:
    print("Error loading Excel:", e)
    df = pd.DataFrame(
        columns=[
            "seating_no",
            "arabic_name",
            "total_degree",
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎓 أهلاً بك في بوت نتيجة الثانوية العامة.

يمكنك البحث بإحدى الطريقتين:

1️⃣ رقم الجلوس
مثال:
123456

2️⃣ الاسم أو جزء من الاسم
مثال:
محمد أحمد

سيتم عرض النتيجة فورًا.
"""

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أرسل رقم الجلوس أو الاسم للبحث."
    )


def search_by_seating(seating):
    result = df[df["seating_no"] == seating]

    if len(result) == 0:
        return None

    return result.iloc[0]


def search_by_name(name):
    result = df[
        df["arabic_name"].str.contains(
            name,
            case=False,
            na=False,
        )
    ]

    return result
def format_result(row):
    return f"""
🎓 نتيجة الثانوية العامة

👤 الاسم:
{row['arabic_name']}

🪪 رقم الجلوس:
{row['seating_no']}

📊 المجموع:
{row['total_degree']}
"""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.isdigit():
        row = search_by_seating(text)

        if row is None:
            await update.message.reply_text(
                "❌ لم يتم العثور على رقم الجلوس."
            )
            return

        await update.message.reply_text(format_result(row))
        return

    result = search_by_name(text)

    if len(result) == 0:
        await update.message.reply_text(
            "❌ لم يتم العثور على الاسم."
        )
        return

    if len(result) > 10:
        await update.message.reply_text(
            "يوجد أكثر من 10 نتائج.\nاكتب الاسم بشكل أدق."
        )
        return

    for _, row in result.iterrows():
        await update.message.reply_text(format_result(row))


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
