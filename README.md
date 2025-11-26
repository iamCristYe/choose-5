# send_first_img

Small script to fetch the first item image from https://www.nogizaka46shop.com/category/426 and send it to a Telegram chat using a bot.

Prerequisites
- Python 3.8+
- Install dependencies:

  pip install -r requirements.txt

Setup
1. Create a bot with BotFather and obtain `TELEGRAM_BOT_TOKEN`.
2. Obtain the target `TELEGRAM_CHAT_ID` (group chat id or channel id). For groups it is usually a negative integer.
3. You can put these in your environment or use a tool like direnv.

Example (bash):

```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="-1001234567890"
python send_first_img.py
```

Files
- `send_first_img.py`: the main script
- `requirements.txt`: Python deps
- `.env.example`: example environment variables

Notes
- The script finds the first `<div id="item_...">` block on the page and uses the first `<img>` it finds inside that block.
- If the site structure changes this script might need updates.
