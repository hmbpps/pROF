import datetime
import os
import collector
# poster modülünü bir sonraki adımda yazacağız

def calistir():
    # Türkiye saati için UTC+3 ayarı (GitHub sunucuları UTC kullanır)
    tsi_saat = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).hour
    
    print(f"Şu anki Türkiye Saati: {tsi_saat}:00")

    if tsi_saat == 18 or tsi_saat == 19:
        # Akşam: Veri topla ve kaydet
        collector.verileri_topla()
    
    elif tsi_saat == 10:
        print("Sabah tweeti: Günün özeti paylaşılıyor...")
        # poster.tweet_at("ozet")
    
    elif tsi_saat == 13:
        print("Öğle tweeti: Teknik sinyaller paylaşılıyor...")
        # poster.tweet_at("teknik")

if __name__ == "__main__":
    calistir()
