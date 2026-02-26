import os
import math
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
m = 26

def mod_inverse(a, m):
    return pow(a, -1, m)

def encrypt_affine(text, a, b):
    text = text.upper()
    res = ""
    for ch in text:
        if ch in ALPHABET:
            t = ALPHABET.index(ch)
            c = (a * t + b) % m
            res += ALPHABET[c]
        else:
            res += ch
    return res

def decrypt_affine(cipher, a, b):
    cipher = cipher.upper()
    a_inv = mod_inverse(a, m)
    res = ""
    for ch in cipher:
        if ch in ALPHABET:
            c = ALPHABET.index(ch)
            t = (a_inv * (c - b)) % m
            res += ALPHABET[t]
        else:
            res += ch
    return res

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Affine bot ishlamoqda!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/encrypt a b matn\n"
        "/decrypt a b matn"
    )

async def encrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        a = int(context.args[0])
        b = int(context.args[1])
        text = " ".join(context.args[2:])

        if math.gcd(a, 26) != 1:
            await update.message.reply_text("❌ a va 26 coprime bo‘lishi kerak")
            return

        cipher = encrypt_affine(text, a, b)
        await update.message.reply_text(cipher)

    except:
        await update.message.reply_text("❌ Format: /encrypt a b matn")

async def decrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        a = int(context.args[0])
        b = int(context.args[1])
        text = " ".join(context.args[2:])

        if math.gcd(a, 26) != 1:
            await update.message.reply_text("❌ a va 26 coprime bo‘lishi kerak")
            return

        plain = decrypt_affine(text, a, b)
        await update.message.reply_text(plain)

    except:
        await update.message.reply_text("❌ Format: /decrypt a b matn")

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("encrypt", encrypt))
    app.add_handler(CommandHandler("decrypt", decrypt))

    print("Bot started...")
    app.run_polling()
