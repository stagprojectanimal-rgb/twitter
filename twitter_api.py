import os
import tweepy
from dotenv import load_dotenv

# --- .env読み込み ---
load_dotenv()

def get_twitter_client():
    """
    Twitter APIクライアントを返す（認証済み）
    """
    try:
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        return client
    except Exception as e:
        print(f"[ERROR] Failed to initialize Twitter client: {e}")
        return None


if __name__ == "__main__":
    # 単体で実行した場合、接続確認を行う
    client = get_twitter_client()
    if client:
        try:
            me = client.get_me()
            print(f"[OK] Connected as: {me.data['username']}")
        except Exception as e:
            print(f"[ERROR] Connection test failed: {e}")
