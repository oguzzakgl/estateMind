import streamlit as st
import pandas as pd
import os
import time
from scraper import scrape_hepsiemlak, save_to_csv
from preprocessor import clean_house_data
from model_trainer import train_house_model
from predictor import yapay_zeka_dosyalarini_yukle

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Emlak Fiyat Tahmin Sistemi",
    page_icon="🏠",
    layout="wide"
)

# --- TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .sonuc-kutusu {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

def ana_program():
    st.sidebar.title("🏠 ANA MENÜ")
    secim = st.sidebar.selectbox(
        "Lütfen bir işlem seçin:",
        ["Fiyat Tahmin Et", "İnternetten Veri Çek", "Yapay Zekayı Eğit"]
    )

    if secim == "Fiyat Tahmin Et":
        st.title("🤖 Emlak Fiyat Tahmini")
        st.write("Evin bilgilerini girerek tahmini piyasa değerini öğrenebilirsiniz.")

        # Kayıtlı dosyaları yükle
        model, sozluk, etiketler = yapay_zeka_dosyalarini_yukle()

        if model is None:
            st.warning("⚠️ Önce yapay zekayı eğitmeniz gerekiyor!")
        else:
            sol, sag = st.columns(2)
            with sol:
                m2 = st.number_input("Metrekare (m2):", min_value=10, value=100)
                oda = st.slider("Oda Sayısı:", 1, 10, 3)
            with sag:
                yas = st.number_input("Bina Yaşı:", min_value=0, value=5)
                semt = st.selectbox("Semt Seçin:", sozluk.classes_)

            if st.button("Hemen Tahmin Et"):
                # Harf bazlı semti sayıya çevir
                semt_no = sozluk.transform([semt])[0]
                
                # Tahmin yap
                bilgiler = pd.DataFrame([[m2, oda, yas, semt_no]], columns=etiketler)
                tahmin = model.predict(bilgiler)[0]
                
                # Sonucu göster
                st.markdown(f"""
                <div class="sonuc-kutusu">
                    <h3>Tahmini Fiyat</h3>
                    <h2 style='color:#3498db'>{tahmin:,.0f} TL</h2>
                </div>
                """, unsafe_allow_html=True)

    elif secim == "İnternetten Veri Çek":
        st.title("🌐 Veri Toplama Merkezi")
        st.write("Emlak sitelerinden güncel ilanları toplar.")
        
        adet = st.slider("Kaç sayfa taransın?", 1, 5, 1)
        
        if st.button("Verileri Toplamaya Başla"):
            with st.spinner("Lütfen bekleyin, veriler çekiliyor..."):
                gelen_veriler = scrape_hepsiemlak(adet)
                if save_to_csv(gelen_veriler):
                    st.success(f"✅ {len(gelen_veriler)} adet yeni ilan başarıyla kaydedildi!")
                else:
                    st.error("❌ Veriler kaydedilirken bir sorun oluştu.")

    elif secim == "Yapay Zekayı Eğit":
        st.title("🧠 Yapay Zekayı Eğit")
        st.write("Toplanan verileri kullanarak sistemin 'akıllanmasını' sağlar.")

        if st.button("Eğitimi Başlat"):
            with st.spinner("Veriler temizleniyor ve eğitim yapılıyor..."):
                temiz_veri = clean_house_data()
                if temiz_veri is not None:
                    model, puan = train_house_model()
                    st.success(f"✅ Eğitim tamamlandı! Başarı oranımız: %{puan*100:.2f}")
                    
                    st.write("---")
                    st.subheader("📊 Eğitim Detayları")
                    k1, k2 = st.columns(2)
                    k1.metric("Kullanılan İlan Sayısı", len(temiz_veri))
                    k2.metric("Öğrenilen Semt Sayısı", len(temiz_veri['dist'].unique()))
                else:
                    st.error("❌ Henüz hiç veri toplanmamış!")

if __name__ == "__main__":
    ana_program()
