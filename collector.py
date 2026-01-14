import yfinance as yf
import pandas as pd
import pandas_ta as ta
import json

def verileri_topla():
    # Analiz etmek istediğin hisse listesi (BIST30 örneği)
    hisseler = ["THYAO.IS", "SASA.IS", "EREGL.IS", "ASELS.IS", "KCHOL.IS", "AKBNK.IS", "TUPRS.IS"] # Listeyi uzatabilirsin
    sonuclar = []

    for sembol in hisseler:
        try:
            df = yf.download(sembol, period="1mo", interval="1d")
            if df.empty: continue

            # 1. Günlük Değişim
            kapanis = df['Close'].iloc[-1]
            onceki_kapanis = df['Close'].iloc[-2]
            degisim = ((kapanis - onceki_kapanis) / onceki_kapanis) * 100

            # 2. RSI Hesaplama (14 Günlük)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            guncel_rsi = df['RSI'].iloc[-1]

            # 3. Hacim Analizi (Bugünkü hacim / 10 günlük ortalama hacim)
            ortalama_hacim = df['Volume'].tail(10).mean()
            guncel_hacim = df['Volume'].iloc[-1]
            hacim_orani = guncel_hacim / ortalama_hacim

            sonuclar.append({
                "sembol": sembol.replace(".IS", ""),
                "fiyat": round(float(kapanis), 2),
                "degisim": round(float(degisim), 2),
                "rsi": round(float(guncel_rsi), 2),
                "hacim_artisi": round(float(hacim_orani), 2)
            })
        except Exception as e:
            print(f"{sembol} verisi alınamadı: {e}")

    # Verileri JSON olarak kaydet
    with open('analiz_verileri.json', 'w', encoding='utf-8') as f:
        json.dump(sonuclar, f, ensure_ascii=False, indent=4)
    
    print("Veriler başarıyla analiz_verileri.json dosyasına kaydedildi.")

if __name__ == "__main__":
    verileri_topla()
