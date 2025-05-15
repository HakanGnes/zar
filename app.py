import streamlit as st
import time
import random
import os
import base64
import statistics

# Sayfa başlığı ve stil
st.set_page_config(page_title="Zar Oyunu", page_icon="🎲", layout="centered")

# Bootstrap ve animasyonlu CSS ekle (header'a eklenir)
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
    .dice-anim {
        animation: shake 0.6s;
        animation-iteration-count: 1;
        display: inline-block;
    }
    @keyframes shake {
      0% { transform: translate(2px, 2px) rotate(0deg); }
      10% { transform: translate(-2px, -4px) rotate(-2deg); }
      20% { transform: translate(-6px, 0px) rotate(2deg); }
      30% { transform: translate(6px, 4px) rotate(0deg); }
      40% { transform: translate(2px, -2px) rotate(2deg); }
      50% { transform: translate(-2px, 4px) rotate(-2deg); }
      60% { transform: translate(-6px, 2px) rotate(0deg); }
      70% { transform: translate(6px, 2px) rotate(-2deg); }
      80% { transform: translate(-2px, -2px) rotate(2deg); }
      90% { transform: translate(2px, 4px) rotate(0deg); }
      100% { transform: translate(2px, -4px) rotate(-2deg); }
    }
    .info-card {
        background: #F8F9FA;
        border-radius: 18px;
        padding: 16px;
        margin-top: 10px;
        margin-bottom: 8px;
        box-shadow: 0 2px 16px 0 #c5c7d9;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Ortada tek sütun
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(
        "<h1 class='text-center' style='color: #145A32; font-family: QuickAndRegular;'>Zar Oyunu</h1>",
        unsafe_allow_html=True
    )

    if "zarlar" not in st.session_state:
        st.session_state.zarlar = []

    PNG_PATH = "images"  # PNG'ler app ile aynı dizinde olmalı

    # Zar görselini base64 + animasyonla ortada göster
    def show_dice(num, slot, animate=False):
        img_path = os.path.join(PNG_PATH, f"{num}.png")
        with open(img_path, "rb") as image_file:
            img_bytes = image_file.read()
            encoded = base64.b64encode(img_bytes).decode()
        css_class = "dice-anim" if animate else ""
        slot.markdown(
            f"<div style='display: flex; justify-content: center;'>"
            f"<img src='data:image/png;base64,{encoded}' width='120' class='{css_class}'/>"
            f"</div>", unsafe_allow_html=True
        )

    zar_slot = st.empty()
    show_dice(st.session_state.zarlar[-1] if st.session_state.zarlar else 1, zar_slot)

    st.markdown("<br>", unsafe_allow_html=True)

    # Zar At butonu
    if st.button("🎲 Zar At", use_container_width=True):
        # Animasyon efekti (hızlıca döndür)
        for _ in range(20):
            num = random.randint(1, 6)
            show_dice(num, zar_slot, animate=True)
            time.sleep(0.05)
        # Son zar sonucu
        sonuc = random.randint(1, 6)
        st.session_state.zarlar.append(sonuc)
        show_dice(sonuc, zar_slot, animate=True)
        time.sleep(0.1)  # Animasyonun görsel olarak çalışması için kısa bir bekleme

    # Zar istatistikleri
    if st.session_state.zarlar:
        zarlar = st.session_state.zarlar
        minimum = min(zarlar)
        maksimum = max(zarlar)
        ortalama = round(sum(zarlar) / len(zarlar), 2)
        try:
            mod = statistics.mode(zarlar)
        except statistics.StatisticsError:
            # Eğer tüm zarlar eşit çıktıysa, ilk değeri göster
            mod = zarlar[0]

        st.markdown("""
            <div class="info-card">
                <b>Toplam Atış:</b> {n} <br>
                <b>Minimum:</b> {mn} <br>
                <b>Maksimum:</b> {mx} <br>
                <b>Ortalama (Mean):</b> {mean} <br>
                <b>Mod (En Sık Gelen):</b> {mod}
            </div>
        """.format(n=len(zarlar), mn=minimum, mx=maksimum, mean=ortalama, mod=mod), unsafe_allow_html=True)

        # Atılan zarların tamamını göster
        st.markdown(
            f"<div style='text-align:center; color:#444; margin-top:10px; font-size:16px;'>"
            f"<b>Atılan Zarlar:</b> {', '.join(str(z) for z in zarlar)}"
            f"</div>", unsafe_allow_html=True
        )

    st.markdown(
        "<div style='text-align: center; color: #999; font-size: 15px; margin-top: 18px;'>Made with ❤️ using Streamlit</div>",
        unsafe_allow_html=True
    )




