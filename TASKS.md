# Tasks

> Live queue for **current, pending, and future** work — never history. Completed work belongs in `HISTORY.md`. See `~/.agent/AGENTS.md` → Required Documents.

Status key: `pending | in progress | done | blocked`

## Rules

- Never trample another session's in-flight or pending work.
- Update status as work progresses.
- Only mark `done` after verification (tests pass, behavior confirmed).
- `done` is **transient**: after verification, port the row's substance into `HISTORY.md` and delete the row from `TASKS.md` in the same change.
- If a completed task is worth remembering, that's a `HISTORY.md` entry — not a `TASKS.md` preservation.
- Smell test: if `done` rows outnumber open rows, the file has drifted into a log. Clean it up.
- Keep tasks small and actionable — one unit of work each.

## Open

> Source: README "Roadmap" (unchecked items) and "(planned)" tech-stack entries. No TODO/FIXME markers exist in source. Repo is dormant (last commit 2026-04-09).

### Task 1: AWS Lambda deployment
- **Status:** pending
- **Description:** Package and deploy `src/bot.py` as an AWS Lambda function for serverless execution (README marks this "(planned)").
- **Blocked by:** none
- **Tests:** manual verification
- **Done when:**
  - Bot runs successfully as a Lambda invocation.

### Task 2: DynamoDB integration
- **Status:** pending
- **Description:** Replace the in-memory `processed_comments` set with DynamoDB-backed state so processed comments persist across invocations (README "(planned)"; `src/bot.py` notes "Later this will be DynamoDB").
- **Blocked by:** none
- **Tests:** manual verification
- **Done when:**
  - Processed comment IDs persist between runs via DynamoDB.

### Task 3: EventBridge scheduling
- **Status:** pending
- **Description:** Add EventBridge scheduled trigger to run the bot on the intended 15-minute cycle (README "(planned)"; `main()` notes "Later we'll make this run on a schedule").
- **Blocked by:** Task 1
- **Tests:** manual verification
- **Done when:**
  - Bot is invoked automatically on a recurring schedule.

### Task 4: Enhanced keyword detection
- **Status:** pending
- **Description:** Improve keyword matching beyond the current substring check in `check_for_keywords` (README Roadmap).
- **Blocked by:** none
- **Tests:** manual verification
- **Done when:**
  - Keyword detection handles cases beyond simple substring matches.

### Task 5: Multi-subreddit support
- **Status:** pending
- **Description:** Finalize multi-subreddit handling (README Roadmap lists this as pending; `src/bot.py` already loops over `config.SUBREDDITS` but stops after the first reply per run).
- **Blocked by:** none
- **Tests:** manual verification
- **Done when:**
  - Multiple subreddits are monitored as intended by the roadmap.
