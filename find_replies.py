"""Busca tweets recientes de cuentas de IA para responder a mano. Coste ~0,005 $ por tweet leído."""
import sys
from datetime import datetime, timezone
from common import x_client

ACCOUNTS = ["ollama", "ggerganov", "danielhanchen", "reach_vb", "_akhaliq", "rasbt", "Teknium1",
            "simonw", "jxnlco", "swyx", "bcherny", "levelsio", "emollick"]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40

query = "(" + " OR ".join(f"from:{a}" for a in ACCOUNTS) + ") -is:reply -is:retweet"
r = x_client().search_recent_tweets(
    query=query, max_results=N, sort_order="recency", user_auth=True,
    tweet_fields=["created_at", "public_metrics", "author_id"],
    expansions=["author_id"], user_fields=["username"])
users = {u.id: u.username for u in (r.includes or {}).get("users", [])}
now = datetime.now(timezone.utc)
for t in r.data or []:
    m = t.public_metrics
    mins = int((now - t.created_at).total_seconds() // 60)
    edad = f"{mins} min" if mins < 120 else f"{mins // 60} h"
    print(f"--- @{users.get(t.author_id)} | hace {edad} | {m['reply_count']} resp, {m['like_count']} likes")
    print(t.text.replace("\n", " ")[:300])
    print(f"https://x.com/{users.get(t.author_id)}/status/{t.id}\n")
