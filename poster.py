import tweepy
import json
import os

# GitHub Secrets'dan gelecek olan anahtarlar
API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("X_BEARER_TOKEN")

def x_baglan():
    # X API v2 kullanımı (Free Tier için en stabil yol)
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )
    return client

def tweet_olustur(tip):
    with open('analiz_verileri.json', 'r', encoding='utf-8') as f:
        veriler = json.load(f)
    
    if tip == "ozet":
        # En çok artan 3 hisseyi bul
        sirali = sorted(veriler, key=lambda x: x['degisim'], reverse=True)[:3]
        metin = "🚀 Günün Yıldızları (BIST30):\n\n"
        for h in sirali:
            metin += f"${h['sembol']}: %{h['degisim']} artışla {h['fiyat']} TL\n"
        metin += "\n#BIST100 #BorsaIstanbul #Hisse"
        
    elif tip == "teknik":
        # RSI 30 altı veya 70 üstü olanları bul
        rsi_list = [h for h in veriler if h['rsi'] < 40 or h['rsi'] > 70]
        metin = "📊 Teknik Analiz - RSI Sinyalleri:\n\n"
        if not rsi_list:
            metin += "Şu an ekstrem RSI sinyali veren BIST30 hissesi bulunmuyor."
        for h in rsi_list[:4]:
            durum = "Aşırı Satım" if h['rsi'] < 40 else "Aşırı Alım"
            metin += f"${h['sembol']}: RSI {h['rsi']} ({durum})\n"
        metin += "\n#TeknikAnaliz #RSI"

    return metin

def tweet_at(tip):
    client = x_baglan()
    mesaj = tweet_olustur(tip)
    client.create_tweet(text=mesaj)
    print(f"{tip} tweeti başarıyla gönderildi.")
