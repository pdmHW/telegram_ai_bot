# Telegram AI Bot

A simple AI powered Telegram bot using **Groq API** and **Llama 3.3 70B**. Works in both private chats and group chats.

## Features

- Works in private chats — responds to every message
- Works in group chats — responds when:
  - Message starts with .ai command
  - Bot is mentioned by username
  - Someone replies to the bot
  - Automatically joins interesting discussions
- Remembers conversation history (last 50 messages per user, you can change it code)
- Powered by Groq's ultra-fast Llama 3.3 70B model

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/pdmHW/telegram_ai_bot
cd telegram_ai_bot
```

### 2. Get your API keys
- Telegram Token — open [@BotFather](https://t.me/BotFather) on Telegram and get you Bot Token
- Groq API Key — sign up at [console.groq.com](https://console.groq.com) and create a free API key

### 4. Configure the bot
Open `bot.py` and fill in:

```python
TELEGRAM_TOKEN = "your_telegram_token"
GROQ_API_KEY = "your_groq_api_key"
BOT_USERNAME = "@your_bot_username"

SYSTEM_PROMPT = "You are a helpful assistant."  # Customize this!
```

### 5. Run
```bash
python bot.py
```

## 💡 Usage

| Trigger | Description |
|---|---|
| `.ai <message>` | Ask the bot in a group |
| Reply to bot | Continue the conversation |
| Mention `@botusername` | Tag the bot in a group |
| Any message in DM | Bot always replies in private |

## 📋 Requirements

- Python 3.8+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Telegram Bot Token (free from [@BotFather](https://t.me/BotFather))

## 📄 License

MIT License — free to use, modify and share.
 
