# History

> Back-filled from git history on 2026-06-27 — entries below are reconstructed from commit messages, not contemporaneous notes.

## 2025-11-07 — Initial bot

- Initial commit: Reddit Giphy bot with local-testing version (`src/bot.py`). Monitors configured subreddits via PRAW, matches trigger keywords in recent comments, searches Giphy (pg-13), and replies once per run with a gif. Tracks processed comment IDs in-memory to avoid duplicates. Ships `config.example.py` and `requirements.txt`.
- Added debugging output to the bot run loop.

## 2025-11-12 — Project structure cleanup

- Standardized project structure.
- Updated `.gitignore` to sync `.dev/`.

## 2026-04-09 — Licensing

- Added MIT license file.
