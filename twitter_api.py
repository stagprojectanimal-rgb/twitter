import os
import tweepy


def get_twitter_client():
    """
    Twitter APIクライアントを返す（認証済み）
    GitHub Secrets または環境変数から直接読み取る
    """
    try:
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )
        return client
    except Exception as e:
        print(f"[ERROR] Failed to initialize Twitter client: {e}")
        return None


if __name__ == "__main__":
    # 単体実行でAPI接続を確認
    client = get_twitter_client()
    if client:
        try:
            me = client.get_me()
            print(f"[OK] Connected as: {me.data['username']}")
        except Exception as e:
            print(f"[ERROR] Connection test failed: {e}")
