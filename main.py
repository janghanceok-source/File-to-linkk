import os
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("22993457"))
API_HASH = os.getenv("c4e87efc07ddee8948acf641ee297a28")
BOT_TOKEN = os.getenv("8375416782:AAEYO6suD5BPqKKh85BcHe7yp9W_zWp_TnE")

app = Client(
    "DirectLinkBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# -------------------------
#  SIMPLE WEB SERVER FOR RENDER
# -------------------------

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is alive!"

def run_web():
    web.run(host="0.0.0.0", port=8080)

# run flask in background thread
threading.Thread(target=run_web).start()


# -------------------------
# BOT LOGIC
# -------------------------

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text("Send any file — forwarded or normal — I’ll give direct download link.")

@app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo | filters.forwarded))
async def link_generator(client, message: Message):

    file = (
        message.document or
        message.video or
        message.audio or
        message.photo
    )

    if not file:
        return await message.reply("Forwarded file not detected.")

    file_id = file.file_id

    # get file info
    f = await client.get_file(file_id)

    link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{f.file_path}"

    await message.reply_text(
        f"🔗 **Direct Download Link:**\n{link}"
    )


print("🔥 Bot started on Render!")
app.run()