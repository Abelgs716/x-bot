import json, os
from pathlib import Path
from dotenv import load_dotenv
import tweepy

BASE = Path(__file__).parent
load_dotenv(BASE / ".env")
QUEUE = BASE / "queue.json"

def load_queue():
    return json.loads(QUEUE.read_text(encoding="utf-8"))

def save_queue(q):
    QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")

def x_client():
    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_SECRET"],
    )


def log(msg):
    from datetime import datetime
    with open(BASE / "log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")
    print(msg)


def publish_next():
    """Publica el primer elemento de la cola y devuelve el id del primer tweet (o None).

    Un elemento puede ser un texto (tweet suelto) o {"thread": [textos]} (hilo).
    Si un hilo falla a medias, lo que falta se queda en la cola con "reply_to"
    para continuarlo en la siguiente ejecución.
    """
    q = load_queue()
    if not q:
        log("Cola vacía")
        return None
    item = q[0]
    texts = item["thread"] if isinstance(item, dict) else [item]
    reply_to = item.get("reply_to") if isinstance(item, dict) else None
    largos = [t for t in texts if len(t) > 280]
    if largos:
        log(f"ERROR tweet de {len(largos[0])} caracteres, máximo 280: {largos[0][:50]}...")
        raise SystemExit(1)
    client, first_id = x_client(), None
    for i, text in enumerate(texts):
        try:
            resp = client.create_tweet(text=text, in_reply_to_tweet_id=reply_to)
        except Exception as e:
            if i > 0:
                q[0] = {"thread": texts[i:], "reply_to": reply_to}
                save_queue(q)
            log(f"ERROR al publicar ({e}); quedan {len(texts) - i} tweets de este elemento")
            raise
        reply_to = resp.data["id"]
        first_id = first_id or reply_to
        log(f"Publicado {reply_to}: {text[:60]!r}")
    save_queue(q[1:])
    return first_id
