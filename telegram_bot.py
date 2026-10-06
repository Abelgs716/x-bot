"""Bot de Telegram: envías un mensaje y se añade a la cola. /cola, /publicar."""
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from common import load_queue, save_queue, publish_next

OWNER = int(os.environ["TELEGRAM_ALLOWED_USER_ID"])
def ok(u: Update): return u.effective_user.id == OWNER

async def add(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not ok(u): return
    t = u.message.text
    if len(t) > 280: return await u.message.reply_text(f"{len(t)} caracteres, máx 280")
    q = load_queue(); q.append(t); save_queue(q)
    await u.message.reply_text(f"Añadido. En cola: {len(q)}")

async def cola(u, c):
    if not ok(u): return
    q = load_queue()
    txt = lambda t: f"[HILO de {len(t['thread'])}] {t['thread'][0]}" if isinstance(t, dict) else t
    await u.message.reply_text("\n\n".join(f"{i+1}. {txt(t)}" for i, t in enumerate(q)) or "Vacía")

async def publicar(u, c):
    if not ok(u): return
    tid = publish_next()
    if not tid: return await u.message.reply_text("Vacía")
    await u.message.reply_text(f"Publicado: https://x.com/AbelDevX/status/{tid}")

app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
app.add_handler(CommandHandler("cola", cola))
app.add_handler(CommandHandler("publicar", publicar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add))
app.run_polling()
