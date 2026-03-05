import time
import random
import csv
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    """Tarayıcıyı açar ve bot gibi görünmemek için ayarlarını yapar."""
    ayarlar = Options()
    
    # Gerçek bir kişi gibi görünmek için kullanılan tarayıcı kimliği listesi
    tarayici_kimlikleri = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
    ]
    
    secilen_kimlik = random.choice(tarayici_kimlikleri)
    ayarlar.set_preference("general.useragent.override", secilen_kimlik)
    
    # Otomatik test aracı olduğumuzu gizle
    ayarlar.set_preference("dom.webdriver.enabled", False)
    ayarlar.set_preference("useAutomationExtension", False)
    
    # Tarayıcıyı başlat
    driver = webdriver.Firefox(options=ayarlar)
    driver.set_window_size(1366, 768)
    
    # Tarayıcıya "biz bot değiliz" diyen küçük bir kod gönder
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def scrape_hepsiemlak(sayfa_sayisi=1):
    """Belli semtlerdeki kiralık/satılık ilanlarını toplar."""
    semtler = ["besiktas", "kadikoy", "sisli", "eyupsultan", "bayrampasa", "levent"]
    veriler = []
    
    print("🚀 Veri toplama işlemi başlatılıyor...")
    tarayici = get_driver()
    bekleme = WebDriverWait(tarayici, 20)
    
    try:
        for semt in semtler:
            print(f"📍 Şu an buradayız: {semt.upper()}")
            semt_linki = f"https://www.hepsiemlak.com/istanbul-{semt}-satilik-daire"
            
            for sayfa in range(1, sayfa_sayisi + 1):
                url = f"{semt_linki}?page={sayfa}"
                tarayici.get(url)
                
                # Çerez uyarısı çıkarsa "Kabul Et" butonuna bas
                try:
                    cerez_butonu = bekleme.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Kabul Et') or contains(text(),'Anladım')]")))
                    cerez_butonu.click()
                except:
                    pass
                
                # Sayfayı yavaşça aşağı kaydır (Resimler ve ilanlar yüklensin diye)
                tarayici.execute_script("window.scrollTo(0, 800);")
                time.sleep(random.uniform(2, 4))
                
                try:
                    # İlanların yüklenmesini bekle
                    bekleme.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.list-view-line')))
                    ilan_kartlari = tarayici.find_elements(By.CSS_SELECTOR, '.list-view-line')
                    
                    for kart in ilan_kartlari:
                        try:
                            # İlan bilgilerini tek tek çek
                            fiyat = kart.find_element(By.CSS_SELECTOR, '.list-view-price, [class*="price"]').text.strip()
                            konum = kart.find_element(By.CSS_SELECTOR, '.location, .list-view-location').text.strip()
                            
                            baslik_alani = kart.find_element(By.CSS_SELECTOR, '.card-link, a[class*="link"]')
                            baslik = baslik_alani.get_attribute("title")
                            if not baslik:
                                baslik = baslik_alani.text.strip()
                                
                            # Oda sayısı, m2 gibi detayları çek
                            detaylar = kart.find_elements(By.CSS_SELECTOR, '.cel-item, .houseContent span, [class*="cel"]')
                            
                            yeni_veri = {
                                "title": baslik,
                                "location": konum,
                                "room_count": detaylar[0].text.strip() if len(detaylar) > 0 else "N/A",
                                "m2": detaylar[1].text.strip() if len(detaylar) > 1 else "N/A",
                                "building_age": detaylar[2].text.strip() if len(detaylar) > 2 else "N/A",
                                "price": fiyat.replace("\n", " "),
                                "dist": semt,
                                "site": "Hepsiemlak",
                                "date": datetime.now().strftime("%Y-%m-%d")
                            }
                            veriler.append(yeni_veri)
                        except:
                            continue
                    
                    print(f"✅ {semt} semtinden {len(ilan_kartlari)} ilan toplandı.")
                    
                except:
                    # Hata olursa o anki ekranın fotoğrafını çek
                    resim_yolu = f"hata_{semt}_{sayfa}.png"
                    tarayici.save_screenshot(resim_yolu)
                    print(f"❌ {semt} sayfa {sayfa} yüklenirken hata oluştu. Ekran görüntüsü alındı.")
                    
    except Exception as e:
        print(f"⚠️ Bir sorun oluştu: {e}")
    finally:
        tarayici.quit()
        print(f"🏁 İşlem tamam: Toplam {len(veriler)} ilan toplandı.")
    
    return veriler

def save_to_csv(liste):
    """Toplanan verileri bir Excel (CSV) dosyasına kaydeder."""
    if not liste:
        print("💡 Kaydedilecek yeni bir veri yok.")
        return False
        
    dosya_adi = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw_houses.csv")
    
    # Klasör yoksa oluştur
    os.makedirs(os.path.dirname(dosya_adi), exist_ok=True)
    
    dosya_var_mi = os.path.isfile(dosya_adi)
    basliklar = ["title", "location", "room_count", "m2", "building_age", "price", "dist", "site", "date"]
    
    try:
        with open(dosya_adi, mode='a', newline='', encoding='utf-8') as f:
            yazici = csv.DictWriter(f, fieldnames=basliklar)
            if not dosya_var_mi:
                yazici.writeheader()
            yazici.writerows(liste)
        print(f"💾 Veriler '{dosya_adi}' dosyasına eklendi.")
        return True
    except Exception as e:
        print(f"❌ Dosya kaydedilirken hata oldu: {e}")
        return False
