# 🏠 Emlak Fiyat Tahmin Sistemi (Yapay Zeka)

Bu proje, emlak sitelerinden otomatik veri toplayan, bu verileri temizleyen ve yapay zeka kullanarak ev fiyatlarını tahmin eden bir web uygulamasıdır. 

Proje, hem **terminal** üzerinden hem de modern bir **Streamlit** arayüzü üzerinden çalışabilmektedir.

## ✨ Özellikler

- **Veri Toplama (Scraping):** Hepsiemlak gibi sitelerden güncel ilanları çeker.
- **Veri Temizleme:** Hatalı ilanları ayıklar ve m2, fiyat gibi bilgileri düzenler.
- **Yapay Zeka Eğitimi:** Random Forest algoritması kullanarak fiyatları öğrenir.
- **Fiyat Tahmini:** Semt, m2 ve oda sayısına göre tahmini fiyat üretir.

## 🛠️ Kurulum

1. Bilgisayarınızda Python yüklü olduğundan emin olun.
2. Bu klasörü bilgisayarınıza indirin.
3. Terminali (veya CMD) açıp bu klasörün içine gidin.
4. Gerekli kütüphaneleri yüklemek için şu komutu yazın:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Nasıl Çalıştırılır?

### Web Arayüzü İçin (Önerilen)
Web tarayıcınızda görsel bir ekran kullanmak için:
```bash
streamlit run app.py
```

### Terminal (Siyah Ekran) İçin
Sadece kodlarla ilerlemek için:
```bash
python main.py
```

## 📂 Klasör Yapısı

- `app.py`: Ana web arayüzü.
- `main.py`: Ana terminal menüsü.
- `scraper.py`: İnternetten veri çekme kodları.
- `preprocessor.py`: Veri temizleme kodları.
- `model_trainer.py`: Yapay zekayı eğitme kodları.
- `predictor.py`: Tahmin yapma kodları.
- `data/`: Verilerin saklandığı klasör.
- `models/`: Eğitilmiş yapay zeka dosyaları.

---
*Bu proje Python öğrenme sürecinde bir portfolyo projesi olarak geliştirilmiştir.* 😊
