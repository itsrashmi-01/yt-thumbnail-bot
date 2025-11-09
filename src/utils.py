import re, aiohttp
YOUTUBE_REGEXES = [
    r"(?:https?://)?(?:www\.)?youtu\.be/([A-Za-z0-9_-]{6,})",
    r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})",
]
def extract_video_id(text: str):
    for r in YOUTUBE_REGEXES:
        m = re.search(r, text)
        if m:
            return m.group(1)
    m = re.search(r"([A-Za-z0-9_-]{11})", text)
    if m:
        return m.group(1)
    return None
async def head_ok(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                return r.status == 200
    except Exception:
        return False
async def fetch_bytes(url: str):
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                if r.status == 200:
                    return await r.read()
    except Exception:
        return None
