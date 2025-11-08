# Reddit Giphy Bot

A Python bot that monitors Reddit comments and responds with relevant Giphy gifs.

## Features

- Monitors specified subreddits for keyword triggers
- Responds with contextually appropriate gifs from Giphy
- Rate-limited to one response per 15-minute cycle
- Tracks processed comments to avoid duplicates

## Technology Stack

- **Python 3** with PRAW (Reddit API)
- **Giphy API** for gif searches
- **AWS Lambda** for serverless execution (planned)
- **DynamoDB** for state management (planned)
- **EventBridge** for scheduled triggers (planned)

## Current Status

🚧 In Development - Local testing phase

## Setup (Local Testing)

1. Clone the repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `config.py` with your credentials (see config.example.py)
6. Run: `python3 bot.py`

## Configuration

Copy `config.example.py` to `config.py` and fill in your credentials.

**Note:** `config.py` is gitignored to protect your API keys.

## Keywords

Currently responds to:
- Direct requests: "gif me", "show me a gif", "need a gif"
- Soft requests: "cheer me up", "make me laugh", "could use a laugh"

## Project Structure
```
reddit-giphy-bot/
├── bot.py              # Main bot logic
├── config.py           # Credentials (gitignored)
├── config.example.py   # Template for config
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Roadmap

- [x] Local testing script
- [ ] AWS Lambda deployment
- [ ] DynamoDB integration
- [ ] EventBridge scheduling
- [ ] Enhanced keyword detection
- [ ] Multi-subreddit support

## License

Personal project
