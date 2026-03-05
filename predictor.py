import joblib
import pandas as pd
import os

def yapay_zeka_dosyalarini_yukle():
    """models/ klasöründeki eğitilmiş dosyaları programa yükler."""
    ana_dizin = os.path.dirname(os.path.abspath(__file__))
    model_yolu = os.path.join(ana_dizin, "models", "house_price_model.pkl")
    sozluk_yolu = os.path.join(ana_dizin, "models", "district_encoder.pkl")
    etiket_yolu = os.path.join(ana_dizin, "models", "feature_names.pkl")

    # Dosyalar var mı kontrol et
    if not os.path.exists(model_yolu):
        return None, None, None
    
    # Dosyaları yükle
    model = joblib.load(model_yolu)
    sozluk = joblib.load(sozluk_yolu)
    etiketler = joblib.load(etiket_yolu)
    
    return model, sozluk, etiketler

def predict_house_price():
    """
    Kullanıcıdan ev bilgilerini alır ve yapay zekaya fiyat sordurur.
    """
    model, sozluk, etiketler = yapay_zeka_dosyalarini_yukle()
    
    if model is None:
        print("❌ Hata: Kayıtlı yapay zeka dosyası bulunamadı! Lütfen önce eğitimi yapın.")
        return

    print("\n" + "="*40)
    print(" 🏠 EMLAK FİYAT TAHMİN EKRANI 🤖 ")
    print("="*40)

    try:
        # Kullanıcıdan bilgileri iste
        m2 = float(input("Evin metrekaresi (m2): "))
        oda = int(input("Oda sayısı (Toplam): "))
        yas = int(input("Bina yaşı: "))
        
        print("\nBilinen Semtler:", ", ".join(sozluk.classes_))
        semt = input("Semt ismi: ").strip().lower()

        # Semt ismini yapay zekanın anlayacağı numaraya çevir
        try:
            semt_numarasi = sozluk.transform([semt])[0]
        except:
            print(f"⚠️ Uyarı: '{semt}' sistemde kayıtlı değil. Bilinen ilk semt baz alınıyor.")
            semt_numarasi = 0

        # Yapay zekaya bilgileri ver
        # Bilgileri modelin beklediği tablo (DataFrame) formatına koyuyoruz
        bilgiler = pd.DataFrame([[m2, oda, yas, semt_numarasi]], columns=etiketler)
        
        # Tahmin yap
        tahmin = model.predict(bilgiler)[0]

        print("\n" + "-"*40)
        print(f"✅ TAHMİN EDİLEN FİYAT: {tahmin:,.0f} TL")
        print("-"*40)

    except ValueError:
        print("❌ Hata: Lütfen kutucuklara sadece sayı giriniz!")
    except Exception as e:
        print(f"❌ Bir hata oluştu: {e}")
