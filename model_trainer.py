import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

def train_house_model():
    """
    Yapay zeka modelini eğitir ve dosyalar halinde kaydeder.
    """
    # Dosya yollarını ayarla
    ana_dizin = os.path.dirname(os.path.abspath(__file__))
    veri_yolu = os.path.join(ana_dizin, "data", "processed_houses.csv")

    if not os.path.exists(veri_yolu):
        print(f"❌ '{veri_yolu}' bulunamadı! Lütfen önce verileri temizleyin.")
        return None, 0

    # 1. Temiz veriyi yükle
    print("📊 Veriler yükleniyor...")
    veri = pd.read_csv(veri_yolu)
    
    # 2. Semt isimlerini sayılara çevirme (Label Encoding)
    # Bilgisayar 'Kadıköy' kelimesini anlayamaz, ona bir numara vermemiz lazım.
    sozluk = LabelEncoder()
    veri['dist_encoded'] = sozluk.fit_transform(veri['dist'])
    
    print(f"🏷️ Semtler numaralandırıldı: {sozluk.classes_}")
    
    # 3. Giriş ve Çıkış verilerini belirle
    # Bilgisayara m2, oda, yaş ve semti vereceğiz (X)
    # O da bize fiyatı tahmin etmeye çalışacak (y)
    X = veri[['m2', 'rooms', 'age', 'dist_encoded']]
    y = veri['price']

    # 4. Veriyi Eğitim ve Test olarak ikiye böl
    # Verinin %80'i ile öğrenecek, %20'si ile kendini test edecek.
    X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"✂️ Veri bölündü: {len(X_egitim)} egitim, {len(X_test)} test verisi.")

    # 5. Yapay Zekayı Eğit (Random Forest algoritması)
    print("🧠 Yapay zeka eğitiliyor, biraz bekleyin...")
    algoritma = RandomForestRegressor(n_estimators=100, random_state=42)
    algoritma.fit(X_egitim, y_egitim)

    # 6. Başarı puanını hesapla (R2 Skoru)
    tahminler = algoritma.predict(X_test)
    basari_puani = r2_score(y_test, tahminler)
    print(f"✅ Eğitim bitti! Başarı Oranı: %{basari_puani*100:.2f}")

    # 7. Öğrenilenleri 'models' klasörüne dosyalar olarak kaydet (Daha sonra kullanmak için)
    model_klasoru = os.path.join(ana_dizin, "models")
    if not os.path.exists(model_klasoru):
        os.makedirs(model_klasoru)
    
    joblib.dump(algoritma, os.path.join(model_klasoru, "house_price_model.pkl"))
    joblib.dump(sozluk, os.path.join(model_klasoru, "district_encoder.pkl"))
    joblib.dump(list(X.columns), os.path.join(model_klasoru, "feature_names.pkl"))

    print(f"💾 Tüm dosyalar kaydedildi: {model_klasoru}")
    
    return algoritma, basari_puani

if __name__ == "__main__":
    train_house_model()
