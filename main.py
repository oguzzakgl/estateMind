from scraper import scrape_hepsiemlak, save_to_csv
from preprocessor import clean_house_data
from model_trainer import train_house_model
from predictor import predict_house_price

def ana_menu():
    """
    Kullanıcının terminal üzerinden işlemler yapmasını sağlayan menü.
    """
    while True:
        print("\n" + "="*45)
        print("   🏠 EMLAK ANALİZ VE TAHMİN SİSTEMİ   ")
        print("="*45)
        print(" 1. Verileri İnternetten Topla (Scraping)")
        print(" 2. Yapay Zekayı Eğit (Eğitim)")
        print(" 3. Fiyat Tahmini Yap (Tahmin)")
        print(" 4. Programdan Çık")
        print("-"*45)
        
        secim = input(" Bir seçenek girin (1-4): ")

        if secim == '1':
            print("\n🚀 Veri toplama başlıyor...")
            liste = scrape_hepsiemlak(sayfa_sayisi=1)
            if save_to_csv(liste):
                print("✅ İşlem başarıyla bitti.")
            else:
                print("⚠️ Veri toplanamadı.")

        elif secim == '2':
            print("\n🧹 Önce veriler temizleniyor...")
            temiz_df = clean_house_data()
            if temiz_df is not None:
                print("🧠 Şimdi yapay zeka eğitiliyor...")
                train_house_model()
                print("✅ Yapay zeka başarıyla eğitildi!")
            else:
                print("❌ Veri bulunamadığı için eğitim yapılamadı.")

        elif secim == '3':
            # Fiyat tahmin ekranını açar
            predict_house_price()

        elif secim == '4':
            print("\n👋 Görüşmek üzere!")
            break

        else:
            print("\n❌ Yanlış tuşladınız, lütfen 1 ile 4 arasında bir seçim yapın.")

if __name__ == "__main__":
    ana_menu()
