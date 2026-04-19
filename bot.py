import requests
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "TOKEN"
GROQ_API_KEY = "API_KEY"
BOT_USERNAME = "@username"

SYSTEM_PROMPT = "PROMPT" #Enter Prompt here

JUDGE_PROMPT = """Read Telegram messages . Respond only JSON, don't write anything else:
{"should_reply": true/false}

should_reply = true only if:
- There's going crazy discussion 
- Difficult questions 

Unless false."""

chat_histories = {}
group_messages = []

def ask_ai(messages):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages
    }
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    result = res.json()
    print("RESPONSE:", result)
    return result["choices"][0]["message"]["content"]

def should_reply_to(text):
    try:
        result = ask_ai([
            {"role": "user", "content": JUDGE_PROMPT + "\n\n" + text}
        ])
        return '"should_reply": true' in result
    except:
        return False

def get_user_history(user_id):
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    return chat_histories[user_id]

def save_message(user_id, role, content):
    history = get_user_history(user_id)
    history.append({"role": role, "content": content})
    if len(history) > 50:
        chat_histories[user_id] = history[-50:]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "bro"
    is_group = message.chat.type in ["group", "supergroup"]
    bot_id = context.bot.id

    should_respond = False

    if is_group:
        if text.lower().startswith(".ai"):
            should_respond = True
            text = text[3:].strip() or "salom"
        elif message.reply_to_message and message.reply_to_message.from_user.id == bot_id:
            should_respond = True
        elif BOT_USERNAME.lower() in text.lower():
            should_respond = True
            text = text.replace(BOT_USERNAME, "").strip()
        elif random.random() < 0.2:
            group_messages.append(f"{first_name}: {text}")
            if len(group_messages) > 10:
                group_messages.pop(0)
            combined = "\n".join(group_messages)
            if should_reply_to(combined):
                should_respond = True
                text = combined
    else:
        should_respond = True

    if not should_respond:
        return

    user_context = f"{first_name} degan odam yozmoqda: {text}"
    save_message(user_id, "user", user_context)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_user_history(user_id)
    reply = ask_ai(messages)

    save_message(user_id, "assistant", reply)
    await message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot started working")
app.run_polling()

