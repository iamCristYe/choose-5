#!/usr/bin/env python3
"""Fetch the first item image from the Nogizaka46 shop category page and send it to a Telegram chat.

Usage:
  Set environment variables TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID then run:
    python send_first_img.py

Notes:
  - TELEGRAM_CHAT_ID can be a group chat id (negative number) or channel id.
  - The script finds the first <div id="item_..."> on the page, extracts the <img> src and the <dd> caption.
"""
import os
import re
import sys
from typing import Tuple

import requests
from bs4 import BeautifulSoup

URL = "https://www.nogizaka46shop.com/category/426"


def get_first_item(url: str) -> Tuple[str, str]:
    """Return (image_url, caption) for the first item div on the page.

    Raises RuntimeError if not found or on network errors.
    """
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    div = soup.find("div", id=re.compile(r"^item_\d+"))
    if not div:
        raise RuntimeError("No item div found on the page")

    img = div.find("img")
    if not img or not img.get("src"):
        raise RuntimeError("No image tag found in the first item div")

    src = img["src"].strip()
    # Normalize protocol-relative URLs
    if src.startswith("//"):
        src = "https:" + src
    elif src.startswith("/"):
        # Make absolute
        src = requests.compat.urljoin(url, src)

    dd = div.find("dd")
    caption = dd.get_text(strip=True) if dd else ""

    return src, caption


def download_image_bytes(image_url: str) -> bytes:
    resp = requests.get(image_url, timeout=20)
    resp.raise_for_status()
    return resp.content


def send_photo_telegram(bot_token: str, chat_id: str, image_bytes: bytes, caption: str):
    api = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {"photo": ("image.jpg", image_bytes)}
    data = {"chat_id": chat_id, "caption": caption}
    resp = requests.post(api, data=data, files=files, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
        sys.exit(2)

    try:
        image_url, caption = get_first_item(URL)
    except Exception as e:
        print("Error fetching/parsing page:", e)
        sys.exit(1)

    print("Found image:", image_url)
    print("Caption:", caption)

    try:
        image_bytes = download_image_bytes(image_url)
    except Exception as e:
        print("Error downloading image:", e)
        sys.exit(1)

    try:
        res = send_photo_telegram(token, chat_id, image_bytes, caption)
    except Exception as e:
        print("Error sending to Telegram:", e)
        sys.exit(1)

    ok = res.get("ok")
    print("Telegram API returned ok=", ok)


if __name__ == "__main__":
    main()
