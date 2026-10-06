# x-bot

Automate your X (Twitter) account with Python for ~$2/month.

A queue of tweets + a script that posts the next one + Windows Task Scheduler. No server, no SaaS.

## How it works

- `queue.json`: list of items. Each item is a tweet (string) or a thread (`{"thread": [...]}`).
- `post_next.py`: posts the first item and removes it from the queue. Everything is logged to `log.txt`.
- `setup.ps1`: asks for your keys, checks them and schedules the posts.
- `add.py "text"`: adds a tweet to the queue.
- `find_replies.py`: lists recent tweets from AI accounts so you can reply **by hand**.
- `telegram_bot.py` (optional): add tweets to the queue from your phone.

## Setup

1. Create an app at [developer.x.com](https://developer.x.com).
2. In *User authentication settings*, set the permissions to **Read and write**. Do this **before** you generate the tokens.
3. In *Keys and tokens*, copy the **Consumer Keys** (API Key + Secret) and generate the **Access Token + Secret**.
   The OAuth 2.0 Client ID/Secret will **not** work: you'll get a 401.
4. Install the dependencies and run the setup:
   ```
   pip install tweepy python-dotenv python-telegram-bot
   copy queue.example.json queue.json
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```

## Costs (X API pay-per-use, 2026)

| Action | Price |
|---|---|
| Text post | $0.015 |
| Post with a link | $0.20 |
| Read a post | $0.005 |

5 posts/day ≈ $2.25/month. New developer accounts get free credits.

## What NOT to automate

Replies, likes and follows. That's what gets accounts suspended. Automate the posting and do the conversations yourself.
