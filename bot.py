import os
import random
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- Load environment variables ---
load_dotenv()
TOKEN = os.getenv("TOKEN")  # ✅ Must match your .env variable name exactly

if not TOKEN:
    raise ValueError("❌ BOT TOKEN not found! Make sure .env file has TOKEN=xxxx")

# --- Company Info ---
COMPANY_NAME = "BranTech Solutions"
COMPANY_EMAIL = "info@brantechsolutions.co"
COMPANY_PHONE_1 = "+254704894220"
COMPANY_PHONE_2 = "+254759191326"
COMPANY_WEBSITE = "https://brantechsolutions.co"
SERVICES = [
    "Web Design & System Development",
    "Mobile Application Development",
    "Digital Strategy",
    "Branding & Graphic Design",
]

# --- Smart reply tone variations ---
GREETINGS = [
    "Hey there 👋",
    "Hello! 😊",
    "Hi, welcome to BranTech Solutions!",
    "Greetings from BranTech Solutions 🌍",
]

CONFIRMATIONS = [
    "Got you ✅",
    "Sure thing!",
    "Absolutely 👍",
    "Let’s do this 🚀",
]

# --- Keyboard layout ---
main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton("💡 About BranTech"), KeyboardButton("🛠️ Services")],
        [KeyboardButton("📞 Contact Us"), KeyboardButton("🧭 Help")],
    ],
    resize_keyboard=True,
)

# --- Command handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greet = random.choice(GREETINGS)
    await update.message.reply_text(
        f"{greet}\n\n"
        f"I’m your friendly {COMPANY_NAME} assistant.\n"
        f"I can tell you about our *services*, *contact info*, or *who we are*.\n\n"
        "Choose an option below 👇",
        reply_markup=main_menu,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(CONFIRMATIONS)
    await update.message.reply_text(
        f"{msg}\nHere’s what you can ask me:\n"
        "- *About BranTech*\n"
        "- *Our Services*\n"
        "- *Contact Information*\n"
        "- Or just say *Hi!* 😄",
        reply_markup=main_menu,
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💡 *About {COMPANY_NAME}:*\n\n"
        f"{COMPANY_NAME} delivers *innovative technology solutions* for modern businesses.\n"
        "We specialize in building websites, mobile apps, and digital strategies that help your brand stand out.\n\n"
        f"🌐 Visit us at {COMPANY_WEBSITE}",
        reply_markup=main_menu,
    )


async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service_list = "\n".join([f"• {s}" for s in SERVICES])
    await update.message.reply_text(
        f"🛠️ *Our Services:*\n{service_list}\n\n"
        "We blend creativity and technology to transform your ideas into reality 💡\n\n"
        f"Learn more at {COMPANY_WEBSITE}",
        reply_markup=main_menu,
    )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📞 *Contact Us:*\n"
        f"Email: {COMPANY_EMAIL}\n"
        f"Phone: {COMPANY_PHONE_1} / {COMPANY_PHONE_2}\n"
        f"Website: {COMPANY_WEBSITE}\n\n"
        "We’d love to hear from you! 💬",
        reply_markup=main_menu,
    )


# --- Smart auto-reply ---
async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if any(word in text for word in ["hi", "hello", "hey", "start"]):
        await start(update, context)

    elif any(word in text for word in ["help", "assist", "support", "guide"]):
        await help_command(update, context)

    elif any(word in text for word in ["about", "who are you", "brantech", "company"]):
        await about(update, context)

    elif any(word in text for word in ["service", "offer", "develop", "build", "website", "branding"]):
        await services(update, context)

    elif any(word in text for word in ["contact", "email", "phone", "reach", "talk", "call"]):
        await contact(update, context)

    else:
        await update.message.reply_text(
            "🤖 Hmm, I’m not sure I understood that.\n"
            "Try asking about services, contact info, or BranTech Solutions.",
            reply_markup=main_menu,
        )


# --- Main function ---
def main():
    print(f"✅ {COMPANY_NAME} Smart Bot is starting...")
    print(f"Loaded TOKEN: {TOKEN[:10]}...")

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("services", services))
    app.add_handler(CommandHandler("contact", contact))

    # Smart replies (no / needed)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))

    print(f"🤖 {COMPANY_NAME} Smart Bot is running. Listening for messages...")
    app.run_polling()


if __name__ == "__main__":
    main()
