"""
Reddit Giphy Bot - Local Testing Version
Searches Reddit comments for keywords and replies with Giphy gifs
"""

import praw
import requests
import time
from datetime import datetime, timedelta
import config

# ============================================
# SECTION 1: REDDIT CONNECTION
# ============================================

def connect_to_reddit():
    """
    Creates a Reddit instance using PRAW.
    The user_agent is required by Reddit - it identifies your bot.
    Format: platform:app_name:version (by /u/username)
    """
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD,
        user_agent="python:giphy_bot:v1.0 (by /u/{})".format(config.REDDIT_USERNAME)
    )
    
    print(f"✓ Connected to Reddit as u/{reddit.user.me()}")
    return reddit


# ============================================
# SECTION 2: GIPHY INTEGRATION
# ============================================

def search_giphy(search_term, limit=1):
    """
    Searches Giphy for a gif based on search term.
    
    Args:
        search_term: What to search for (e.g., "funny", "cheer up")
        limit: How many results to get (we'll use the first one)
    
    Returns:
        URL of the gif, or None if search fails
    """
    url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": config.GIPHY_API_KEY,
        "q": search_term,
        "limit": limit,
        "rating": "pg-13"  # Keep it appropriate
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises error for bad status codes
        
        data = response.json()
        
        if data['data'] and len(data['data']) > 0:
            gif_url = data['data'][0]['url']  # Get first result
            print(f"  ✓ Found gif: {gif_url}")
            return gif_url
        else:
            print(f"  ✗ No gifs found for '{search_term}'")
            return None
            
    except Exception as e:
        print(f"  ✗ Giphy error: {e}")
        return None


# ============================================
# SECTION 3: KEYWORD MATCHING
# ============================================

def check_for_keywords(comment_text):
    """
    Checks if comment contains any of our trigger keywords.
    
    Args:
        comment_text: The text of the Reddit comment (lowercased)
    
    Returns:
        Tuple of (keyword_found, search_term) or (None, None)
    """
    comment_lower = comment_text.lower()
    
    for keyword, search_term in config.KEYWORDS.items():
        if keyword in comment_lower:
            return (keyword, search_term)
    
    return (None, None)


# ============================================
# SECTION 4: MAIN BOT LOGIC
# ============================================

def run_bot(reddit, processed_comments):
    """
    Main bot logic: Check comments and reply to first match.
    
    Args:
        reddit: PRAW Reddit instance
        processed_comments: Set of comment IDs we've already replied to
    
    Returns:
        True if we replied to a comment, False otherwise
    """
    
    print(f"\n{'='*50}")
    print(f"Bot run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    # Get a timestamp for 15 minutes ago
    # We only want comments from the last 15 minutes
    fifteen_min_ago = datetime.now(datetime.UTC) - timedelta(minutes=15)
    fifteen_min_timestamp = fifteen_min_ago.timestamp()
    
    # Track if we've replied this run
    replied_this_run = False
    
    # Check each subreddit
    for subreddit_name in config.SUBREDDITS:
        if replied_this_run:
            break  # Already replied, stop checking
        
        print(f"\nChecking r/{subreddit_name}...")
        subreddit = reddit.subreddit(subreddit_name)
        
        try:
            # Get recent comments (PRAW gets newest first)
            # Limit to 100 to avoid excessive API calls
            comments = subreddit.comments(limit=100)
            
            comments_checked = 0
            comments_in_timeframe = 0
            
            for comment in comments:
                # Stop if we already replied
                if replied_this_run:
                    break
                
                # Debug: Show what we're checking
                comment_age_minutes = (datetime.now(datetime.UTC).timestamp() - comment.created_utc) / 60
                
                # Skip if comment is older than 15 minutes
                if comment.created_utc < fifteen_min_timestamp:
                    continue
                
                comments_in_timeframe += 1
                
                # Skip if we've already processed this comment
                if comment.id in processed_comments:
                    print(f"  - Skipping already processed comment {comment.id}")
                    continue
                
                # Skip if this is our own comment
                if comment.author and comment.author.name == config.REDDIT_USERNAME:
                    print(f"  - Skipping our own comment")
                    continue
                
                comments_checked += 1
                
                # Debug: Show each comment we're checking
                author_name = comment.author.name if comment.author else "[deleted]"
                comment_preview = comment.body[:60].replace('\n', ' ')
                print(f"  - Checking comment by u/{author_name} ({comment_age_minutes:.1f}m old): '{comment_preview}'")
                
                # Check for keywords
                keyword, search_term = check_for_keywords(comment.body)
                
                if keyword:
                    print(f"\n  ★ MATCH FOUND!")
                    print(f"    Comment by u/{comment.author}: '{comment.body[:50]}...'")
                    print(f"    Keyword: '{keyword}' → Searching Giphy for '{search_term}'")
                    
                    # Search Giphy
                    gif_url = search_giphy(search_term)
                    
                    if gif_url:
                        # Reply to the comment
                        try:
                            reply_text = f"{gif_url}\n\n---\n^(🤖 bot)"
                            comment.reply(reply_text)
                            
                            print(f"  ✓ REPLIED successfully!")
                            
                            # Mark as processed
                            processed_comments.add(comment.id)
                            replied_this_run = True
                            break  # Stop checking more comments
                            
                        except Exception as e:
                            print(f"  ✗ Failed to reply: {e}")
                    else:
                        print(f"  ✗ Skipping - no gif found")
            
            if not replied_this_run:
                print(f"  Checked {comments_checked} recent comments ({comments_in_timeframe} in timeframe), no matches")
        
        except Exception as e:
            print(f"  ✗ Error checking r/{subreddit_name}: {e}")
    
    if not replied_this_run:
        print(f"\nNo matching comments found this run")
    
    return replied_this_run


# ============================================
# SECTION 5: MAIN EXECUTION
# ============================================

def main():
    """
    Main entry point - runs the bot once for testing.
    Later we'll make this run on a schedule.
    """
    print("Starting Reddit Giphy Bot (Local Test Mode)")
    print("=" * 50)
    
    # Connect to Reddit
    reddit = connect_to_reddit()
    
    # Track processed comments (in-memory for now)
    # Later this will be DynamoDB
    processed_comments = set()
    
    # Run bot once
    run_bot(reddit, processed_comments)
    
    print("\n" + "="*50)
    print("Bot run complete!")
    print(f"Total comments processed: {len(processed_comments)}")


if __name__ == "__main__":
    main()
