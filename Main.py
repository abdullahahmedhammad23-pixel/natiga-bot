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
    df = pd.read_excel(EXCEL_FILE, dtype=str)
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
