import logging
from pyrogram import Client
from src.config import Config
from src.db import init_db
from src.handlers import register_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    init_db()
    app = Client('ytthumbbot', bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)
    register_handlers(app)
    logger.info('Starting %s', Config.BOT_NAME)
    app.run()

if __name__ == '__main__':
    main()
