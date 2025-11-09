import logging
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .utils import extract_video_id, fetch_bytes, head_ok
from .db import ensure_user, db
from .config import Config

logger = logging.getLogger(__name__)


def start_markup():
    """Build start message buttons."""
    link = None
    if Config.FORCE_CHANNEL and Config.FORCE_CHANNEL.startswith("@"):
        link = f"https://t.me/{Config.FORCE_CHANNEL.lstrip('@')}"
    buttons = [
        [InlineKeyboardButton("🔰 About Bot", callback_data="about")],
        [InlineKeyboardButton("📢 Update Channel", url=link if link else Config.FORCE_CHANNEL)],
        [InlineKeyboardButton("⚙️ More", callback_data="more")],
    ]
    return InlineKeyboardMarkup(buttons)


def thumb_markup(vid, url):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 Open Image", url=url),
         InlineKeyboardButton("📁 Send as File", callback_data=f"sendfile:{vid}")],
        [InlineKeyboardButton("🔁 More", callback_data="more")]
    ])


def register_handlers(app):
    """Register all bot handlers."""

    @app.on_message(filters.private & filters.command("start"))
    async def start_handler(c, m):
        user = m.from_user
        if db:
            await ensure_user(db.users, user)
        await log_start(c, user)
        text = f"👋 Hi {user.first_name or 'there'}!\n\nI am <b>{Config.BOT_NAME}</b>.\nSend me a YouTube link and I’ll return the video thumbnail."
        markup = start_markup()
        try:
            if Config.START_PIC:
                await m.reply_photo(Config.START_PIC, caption=text, reply_markup=markup)
            else:
                await m.reply_text(text, reply_markup=markup)
        except Exception as e:
            logger.exception("Failed to send start message: %s", e)
            await m.reply_text(text, reply_markup=markup)

    @app.on_message(filters.private & filters.regex(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)"))
    async def yt_handler(c, m):
        user = m.from_user
        if db:
            await ensure_user(db.users, user)
        vid = extract_video_id(m.text or m.caption or "")
        if not vid:
            await m.reply_text("❌ Couldn't detect YouTube video ID.")
            return
        # Check subscription
        joined = await is_member(c, user.id)
        if not joined:
            link = Config.FORCE_CHANNEL if not (Config.FORCE_CHANNEL or "").startswith("@") else f"https://t.me/{Config.FORCE_CHANNEL.lstrip('@')}"
            await m.reply_text("🔒 Please join the update channel to use this bot.",
                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel", url=link)]]))
            return

        # Get thumbnail
        urls = [
            f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg",
            f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
            f"https://img.youtube.com/vi/{vid}/sddefault.jpg"
        ]
        chosen = None
        for u in urls:
            if await head_ok(u):
                chosen = u
                break
        if not chosen:
            await m.reply_text("❌ Couldn't fetch thumbnail. Try again later.")
            return

        await m.reply_photo(chosen, caption=f"📸 Thumbnail for video ID: `{vid}`", reply_markup=thumb_markup(vid, chosen))

    @app.on_callback_query()
    async def cb(c, q):
        data = q.data or ""
        if data.startswith("sendfile:"):
            vid = data.split(":", 1)[1]
            if not await is_member(c, q.from_user.id):
                await q.answer("Please join the update channel first.", show_alert=True)
                return
            urls = [
                f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg",
                f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            ]
            file_bytes = None
            for u in urls:
                file_bytes = await fetch_bytes(u)
                if file_bytes:
                    break
            if not file_bytes:
                await q.answer("Failed to download thumbnail.", show_alert=True)
                return
            await q.message.reply_document(file_bytes, file_name=f"{vid}.jpg", caption=f"🎞️ Thumbnail for {vid}")
            await q.answer("Sent as file ✔️")
            if Config.LOG_CHANNEL:
                try:
                    await c.send_message(Config.LOG_CHANNEL,
                        f"📥 {q.from_user.first_name} ({q.from_user.id}) downloaded thumbnail for {vid}")
                except Exception:
                    pass
        elif data == "about":
            await q.message.edit_text(f"<b>About {Config.BOT_NAME}</b>\n\nA simple YouTube Thumbnail Downloader bot built with Pyrogram.",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❮ Back", callback_data="back")]]))
            await q.answer()
        elif data == "more":
            await q.message.edit_text("More features coming soon...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❮ Back", callback_data="back")]]))
            await q.answer()
        elif data == "back":
            try:
                # Try to restore start message (if possible)
                await q.message.edit_text("👋 Welcome back!", reply_markup=start_markup())
            except Exception:
                await q.answer()
            await q.answer()

    async def is_member(client, user_id: int) -> bool:
        """Check if user joined force-subscribe channel."""
        if not Config.FORCE_CHANNEL:
            return True
        try:
            member = await client.get_chat_member(Config.FORCE_CHANNEL, user_id)
            return member.status not in ("left", "kicked")
        except Exception:
            return False

    async def log_start(client, user):
        """Log new user start."""
        if not Config.LOG_CHANNEL:
            return
        txt = (f"🟢 New /start\n"
               f"User: <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
               f"ID: <code>{user.id}</code>\n"
               f"Bot: {Config.BOT_NAME}")
        try:
            await client.send_message(Config.LOG_CHANNEL, txt)
        except Exception:
            pass