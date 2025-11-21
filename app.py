import streamlit as st
import pandas as pd
import datetime
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="FitRank: Sosyal Egzersiz", page_icon="💪", layout="wide")

# --- SESSION STATE (Verilerin hafızada tutulması için) ---
if 'puan' not in st.session_state:
    st.session_state['puan'] = 0
if 'gun_sayisi' not in st.session_state:
    st.session_state['gun_sayisi'] = 0
if 'seviye' not in st.session_state:
    st.session_state['seviye'] = "🌱 Başlangıç"

# --- FONKSİYONLAR ---
def kategori_belirle(puan, gun):
    if puan > 5000 and gun > 180:
        return "👑 Elit (Legend)"
    elif puan > 2000 and gun > 30:
        return "🔥 Profesyonel"
    elif puan > 500 and gun > 7:
        return "🏃 Amatör"
    else:
        return "🌱 Başlangıç"

def vki_hesapla(kilo, boy):
    boy_m = boy / 100
    vki = kilo / (boy_m ** 2)
    return vki

# --- YAN MENÜ (PROFİL) ---
with st.sidebar:
    st.header("👤 Profil Bilgileri")
    isim = st.text_input("Adın Soyadın", "Misafir Sporcu")
    yas = st.slider("Yaşın", 10, 80, 25)
    boy = st.number_input("Boy (cm)", 100, 250, 180)
    kilo = st.number_input("Kilo (kg)", 30, 200, 80)
    
    vki = vki_hesapla(kilo, boy)
    
    st.divider()
    st.metric(label="Vücut Kitle İndeksi (VKİ)", value=f"{vki:.2f}")
    
    if vki < 18.5:
        st.info("Durum: Zayıf - Kilo alma odaklı program önerilir.")
    elif 18.5 <= vki < 25:
        st.success("Durum: İdeal - Form koruma ve kas yapma.")
    elif 25 <= vki < 30:
        st.warning("Durum: Fazla Kilolu - Kardiyo ağırlıklı program.")
    else:
        st.error("Durum: Obez - Doktor kontrolünde başlangıç.")

# --- ANA EKRAN ---
st.title(f"💪 FitRank: Hoşgeldin {isim}")

# Üst Bilgi Kartları
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Mevcut Kategori", value=st.session_state['seviye'])
with col2:
    st.metric(label="Toplam Puan (XP)", value=st.session_state['puan'])
with col3:
    st.metric(label="Antrenman Günü", value=f"{st.session_state['gun_sayisi']} Gün")

# Sekmeler
tab1, tab2, tab3 = st.tabs(["🏋️ Günlük Egzersiz", "📅 Geçmiş & İstatistik", "🏆 Liderlik Tablosu"])

# --- TAB 1: EGZERSİZ PROGRAMI ---
with tab1:
    st.subheader(f"Bugünün Programı ({datetime.date.today()})")
    st.write("Hareketleri tamamladıkça kutucukları işaretle ve puan kazan!")
    
    # Egzersiz Verisi (Örnek Videolar)
    egzersizler = [
        {"ad": "Şınav (Push-up)", "set": "3x12", "puan": 20, "video": "https://www.youtube.com/watch?v=IODxDxX7oi4"},
        {"ad": "Squat (Çökme)", "set": "4x10", "puan": 25, "video": "https://www.youtube.com/watch?v=YaXPRqUwItQ"},
        {"ad": "Plank", "set": "3x45 sn", "puan": 30, "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
    ]
    
    for egzersiz in egzersizler:
        with st.expander(f"🔥 {egzersiz['ad']} - {egzersiz['set']} (Video İzle)"):
            st.video(egzersiz['video'])
            st.write(f"Tamamlarsan: **+{egzersiz['puan']} Puan**")
            
            if st.button(f"✅ {egzersiz['ad']} Tamamlandı", key=egzersiz['ad']):
                st.session_state['puan'] += egzersiz['puan']
                st.success(f"Tebrikler! {egzersiz['puan']} puan eklendi.")
                # Seviye güncelleme kontrolü
                yeni_seviye = kategori_belirle(st.session_state['puan'], st.session_state['gun_sayisi'])
                if yeni_seviye != st.session_state['seviye']:
                    st.session_state['seviye'] = yeni_seviye
                    st.balloons() # Konfeti efekti
                    st.toast(f"TEBRİKLER! YENİ SEVİYE: {yeni_seviye}")

    if st.button("📅 Günü Bitir ve Kaydet"):
        st.session_state['gun_sayisi'] += 1
        st.session_state['puan'] += 50 # Gün bitirme bonusu
        st.success("Günlük antrenman tamamlandı! +50 Bonus Puan eklendi.")

# --- TAB 2: GEÇMİŞ ---
with tab2:
    st.subheader("Aylık Takvim ve İlerleme")
    # Görsel bir takvim simülasyonu
    data = {
        'Tarih': [datetime.date.today() - datetime.timedelta(days=i) for i in range(5)],
        'Durum': ['Yapıldı', 'Yapıldı', 'Atlandı', 'Yapıldı', 'Yapıldı'],
        'Puan': [150, 140, 0, 160, 120]
    }
    df_gecmis = pd.DataFrame(data)
    st.dataframe(df_gecmis, use_container_width=True)
    
    st.line_chart(df_gecmis.set_index('Tarih')['Puan'])
# --- TAB 3: SOSYAL & LİDERLİK ---
with tab3:
    st.subheader("🏆 Liderlik Tablosu (Global)")
    
    # Kullanıcının kendi kategorisine göre filtreleme
    kategori = st.session_state['seviye']
    st.info(f"Şu an **{kategori}** ligindeki rakiplerini görüyorsun. Mesajlaşmak için birine tıkla.")
    
    # Sahte veri oluşturma (Simülasyon)
    rakipler = {
        'Sıra': [1, 2, 3, 4, 5],
        'Kullanıcı': ['Ahmet_Fit', 'Zeynep99', 'DemirBilek', isim, 'Ece_Koşar'],
        'Kategori': [kategori, kategori, kategori, kategori, kategori],
        'Puan': [st.session_state['puan'] + 500, st.session_state['puan'] + 200, st.session_state['puan'] + 50, st.session_state['puan'], st.session_state['puan'] - 100]
    }
    df_lider = pd.DataFrame(rakipler)
    
    st.dataframe(df_lider, use_container_width=True)    
    st.write("---")
    st.subheader("💬 Lig Sohbet Odası")
    mesaj = st.text_input("Mesajın...")
    if st.button("Gönder"):
        st.write(f"**{isim}:** {mesaj}")
        st.write("**Zeynep99:** Harikasın, aynen devam! 💪")
