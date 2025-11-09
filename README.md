# 🎬 YT Thumbnail Downloader Bot

A professional **Telegram Bot** built using [Pyrogram](https://docs.pyrogram.org/) and **MongoDB**, designed to fetch and download **YouTube video thumbnails** in HD.

> 🧩 Fully asynchronous • ☁️ Deployable on [Koyeb](https://www.koyeb.com) • 🐳 Docker-ready • 🔒 Force Subscribe System Included  

---

## 🧠 Features

- 🖼️ Extracts **high-quality YouTube thumbnails** (maxres / HQ / SD).
- 🔒 **Force Subscribe** system (join update channel before use).
- 👋 Personalized `/start` message with image, user name & buttons.
- 📜 **Log channel support** (user join logs, actions, bot status).
- ⚙️ **MongoDB** integration for users and analytics.
- 📊 **Admin commands:** `/stats`, `/setupdatechannel`, `/setlog`, `/broadcast`.
- ☁️ **24×7 Uptime** — Deployable on Koyeb or any Docker host.
- 🧩 **Modular folder structure** for scalability & easy updates.

---

## 📁 Folder Structure

```
yt-thumbnail-bot/
├── src/
│   ├── config.py        # Configuration loader
│   ├── db.py            # MongoDB initialization
│   ├── handlers.py      # Bot handlers (start, YouTube, callbacks)
│   ├── utils.py         # Helper functions
│   └── __init__.py
├── .env.example         # Example environment file
├── Dockerfile           # Docker build instructions
├── Procfile             # For BotClusters or worker mode
├── requirements.txt     # Dependencies list
├── run.py               # Entrypoint script
└── README.md
```

---

## ⚙️ Environment Variables

Copy `.env.example` → `.env` and fill your details 👇

```env
BOT_TOKEN=123456:ABC-DEF
API_ID=123456
API_HASH=yourapihash
MONGO_URI=mongodb+srv://user:pass@cluster0.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ytthumbbot
FORCE_CHANNEL=@YourUpdateChannel
LOG_CHANNEL=-1001234567890
START_PIC=https://example.com/welcome.jpg
BOT_NAME=YTThumbBot
OWNER_ID=123456789
```

| Key | Description |
|-----|-------------|
| `BOT_TOKEN` | Telegram Bot token from [@BotFather](https://t.me/BotFather) |
| `API_ID` / `API_HASH` | From [my.telegram.org/apps](https://my.telegram.org/apps) |
| `MONGO_URI` | MongoDB Atlas connection URI |
| `DB_NAME` | Database name |
| `FORCE_CHANNEL` | Channel username or ID for force subscription |
| `LOG_CHANNEL` | Channel ID for bot logs |
| `START_PIC` | Welcome image URL |
| `BOT_NAME` | Bot display name |
| `OWNER_ID` | Your Telegram numeric ID (for admin access) |

---

## 🧰 Local Setup

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup `.env`
```bash
cp .env.example .env
# Edit and add your real values
```

### 3️⃣ Run the bot
```bash
python run.py
```

✅ You’ll see:
```
INFO: Starting YTThumbBot
Bot is now running. Press Ctrl+C to stop.
```

---

## 🐳 Docker Deployment

### Build the image
```bash
docker build -t ytthumbbot .
```

### Run the container
```bash
docker run --env-file .env ytthumbbot
```

---

## ☁️ Deploy on Koyeb (24×7 Uptime)

1. Push your project to a **private GitHub repo**.
2. Go to [Koyeb.com](https://www.koyeb.com) → **Create App**.
3. Choose **GitHub → Select your repo**.
4. Koyeb auto-detects the `Dockerfile`.
5. Add the environment variables (same as `.env`).
6. Click **Deploy** 🎉

🟢 Koyeb keeps your bot running 24×7 automatically.

---

## 📊 MongoDB Setup (Atlas)

1. Visit [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Create a **Free Shared Cluster**.
3. Add user credentials and whitelist IP `0.0.0.0/0`.
4. Get the connection string, e.g.:
   ```
   mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority
   ```
5. Paste it into `.env` as `MONGO_URI`.

---

## 🔒 Force Subscribe Setup

1. Create a **Telegram Channel** for updates.
2. Add your bot as **Admin** to that channel.
3. Add channel username (e.g. `@YTThumbUpdates`) in `.env` → `FORCE_CHANNEL`.
4. When a user sends a YouTube URL:
   - ✅ If joined → bot sends thumbnail.
   - ❌ If not → asks to join channel.

---

## 👑 Admin Commands

| Command | Description |
|----------|-------------|
| `/stats` | Show total users and recent ones |
| `/setupdatechannel` | Change force-subscribe channel |
| `/setlog` | Change log channel |
| `/broadcast` | Send message to all users (owner only) |

---

## 📜 Logging

Logs user activity to your log channel:
```
🟢 New /start
User: @username (ID: 123456789)
Bot: YTThumbBot
```

---

## 💡 Customization

You can easily modify:
- Welcome text or image (`START_PIC`)
- Inline buttons and callback text
- Add inline search or YouTube metadata
- Add premium or subscription features

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Framework | Pyrogram |
| Database | MongoDB (Motor) |
| Language | Python 3.11 |
| Hosting | Koyeb |
| Container | Docker |

---

## 🧑‍💻 Developer

**YT Thumbnail Downloader Bot**  
Developed by [Your Name or Team Name]  
📬 Telegram: [@YourTelegramUsername](https://t.me/YourTelegramUsername)  
📢 Updates: [@YourUpdateChannel](https://t.me/YourUpdateChannel)

---

## 🪪 License

```
MIT License
Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 🧠 Troubleshooting

| Problem | Solution |
|----------|-----------|
| Bot doesn’t respond | Check `.env` values and MongoDB connection |
| Force-subscribe not working | Ensure bot is **admin** in channel |
| MongoDB connection error | Whitelist IP `0.0.0.0/0` |
| Bot restarts on Koyeb | View **Logs tab** for detailed error trace |

---

✨ **Deploy once — stay live forever!**
