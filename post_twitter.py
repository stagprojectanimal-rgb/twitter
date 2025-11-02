import random
import os
from twitter_api import get_twitter_client  # ← 追加

# --- 設定エリア ---
# 実際の投稿を有効にする場合は True に変更
ENABLE_TWEET = False

# データファイルパス
TWEET_FILE = os.path.join("twitter", "data", "mr_dog_tweets.txt")
RECENT_FILE = os.path.join("twitter", "data", "recent_ids.txt")

# 直近ツイート数を記録する範囲
RECENT_LIMIT = 100


def load_tweets(path):
    """mr_dog_tweets.txt を読み込み、番号と本文を辞書化"""
    tweets = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                idx, text = line.strip().split("|", 1)
                tweets[int(idx)] = text.strip()
    return tweets


def load_recent_ids(path):
    """recent_ids.txt から最近使った番号リストを取得"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]


def save_recent_ids(path, recent_ids):
    """最近使ったツイート番号を保存"""
    with open(path, "w", encoding="utf-8") as f:
        for i in recent_ids:
            f.write(str(i) + "\n")


def select_random_tweet(tweets, recent_ids):
    """直近100件を避けてランダムにツイートを選ぶ"""
    available = [i for i in tweets.keys() if i not in recent_ids]
    if not available:
        available = list(tweets.keys())  # 全件使用済みならリセット
    tweet_id = random.choice(available)
    return tweet_id, tweets[tweet_id]


def post_tweet(text):
    """Twitterに投稿"""
    client = get_twitter_client()
    if not client:
        print("[ERROR] Twitter client not initialized.")
        return False

    try:
        response = client.create_tweet(text=text)
        print(f"[SUCCESS] Tweet posted! ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to post tweet: {e}")
        return False


def main():
    tweets = load_tweets(TWEET_FILE)
    recent_ids = load_recent_ids(RECENT_FILE)

    tweet_id, text = select_random_tweet(tweets, recent_ids)
    print(f"[SELECTED] #{tweet_id}: {text}\n")

    # --- 投稿部分 ---
    if ENABLE_TWEET:
        print("[INFO] 実際の投稿を開始します...")
        success = post_tweet(text)
        if success:
            print("[INFO] 投稿が完了しました。")
    else:
        print("[DEBUG] 投稿は無効です。以下の内容がツイートされる想定です:")
        print(text)

    # --- recent_ids更新 ---
    recent_ids.append(tweet_id)
    if len(recent_ids) > RECENT_LIMIT:
        recent_ids = recent_ids[-RECENT_LIMIT:]
    save_recent_ids(RECENT_FILE, recent_ids)


if __name__ == "__main__":
    main()
