import pandas as pd
import numpy as np
import re
import os

def deger_temizle(deger):
    """
    Metin içindeki sayıları ayıklar.
    Örn: '1.500.000 TL' -> 1500000.0
    """
    if pd.isna(deger) or deger == "N/A":
        return 0.0
    
    # Sadece rakamları al
    temiz_metin = re.sub(r'[^\d]', '', str(deger))
    
    if temiz_metin == "":
        return 0.0
    else:
        return float(temiz_metin)

def oda_sayisi_bul(oda_metni):
    """
    '3+1' gibi ifadeleri toplar: 3+1 = 4
    """
    if pd.isna(oda_metni) or oda_metni == "N/A":
        return 0
    
    # Metin içindeki sayıları bul (Örn: '3+1' -> ['3', '1'])
    sayilar = re.findall(r'\d+', str(oda_metni))
    
    toplam = 0
    for s in sayilar:
        toplam = toplam + int(s)
    
    if toplam == 0:
        return 1 # Hiç sayı yoksa (Stüdyo gibi) en az 1 oda diyelim
    else:
        return toplam

def clean_house_data():
    """
    Ham verileri (raw_houses.csv) okur, temizler ve yeni bir dosyaya kaydeder.
    """
    # Dosya yollarını ayarla
    ana_dizin = os.path.dirname(os.path.abspath(__file__))
    ham_veri_yolu = os.path.join(ana_dizin, "data", "raw_houses.csv")
    temiz_veri_yolu = os.path.join(ana_dizin, "data", "processed_houses.csv")

    if not os.path.exists(ham_veri_yolu):
        print(f"❌ '{ham_veri_yolu}' dosyası bulunamadı!")
        return None

    # Veriyi oku
    print("⚙️ Veriler temizleniyor...")
    df = pd.read_csv(ham_veri_yolu)

    # Temizlik işlemlerini yap
    df['price'] = df['price'].apply(deger_temizle)
    df['m2'] = df['m2'].apply(deger_temizle)
    df['rooms'] = df['room_count'].apply(oda_sayisi_bul)
    
    # Bina yaşını bul (Metin içinden sadece ilk sayıyı al)
    def yas_bul(metin):
        bulunan = re.search(r'\d+', str(metin))
        if bulunan:
            return int(bulunan.group())
        else:
            return 0
            
    df['age'] = df['building_age'].apply(yas_bul)

    # Hatalı veya aşırı uçlardaki verileri sil (Filtreleme)
    onceki_sayi = len(df)
    
    # Çok ucuz, çok küçük veya odasız evleri atalım
    df = df[df['price'] > 500000]
    df = df[df['m2'] > 20]
    df = df[df['rooms'] > 0]
    
    sonraki_sayi = len(df)
    print(f"🧹 Temizlik bitti. {onceki_sayi - sonraki_sayi} adet hatalı ilan silindi.")

    # Temiz veriyi kaydet
    os.makedirs(os.path.dirname(temiz_veri_yolu), exist_ok=True)
    df.to_csv(temiz_veri_yolu, index=False)
    print(f"✅ Temiz veri şuraya kaydedildi: {temiz_veri_yolu}")
    
    return df
