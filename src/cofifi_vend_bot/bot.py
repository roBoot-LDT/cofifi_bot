#!/usr/bin/env python
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.request import HTTPXRequest

from config import TOKEN
from database import init_db
from handlers import start, feedback, refund

load_dotenv()


def main():
    init_db()
    proxy = os.getenv("PROXY_URL")  # например socks5://user:pass@host:port
    request = HTTPXRequest(proxy=proxy) if proxy else HTTPXRequest()
    app = ApplicationBuilder().token(TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start.start_handler))
    app.add_handler(feedback.conv_handler)
    app.add_handler(refund.conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
