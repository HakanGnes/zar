import streamlit as st
import time
import random
import os
import base64
import statistics

# Tema rengi seçimi (light/dark)
st.set_page_config(page_title="Zar Oyunu", page_icon="🎲", layout="centered")

THEMES = {
    "Açık": {
        "bg": "#F8F9FA",
        "header": "#13592a",
        "text": "#222",
        "card": "#ffffff",
        "shadow": "#c5c7d9"
    },
    "Koyu": {
        "bg": "#2d333b",
        "header": "#13e360",
        "text": "#fafbfc",
        "card": "#22272e",
        "shadow": "#0f1114"
    }
}

st.sidebar.title("Ayarlar")
tema = st.sidebar.selectbox("Tema Seçimi", list(THEMES.keys()))
renk = THEMES[tema]

st.markdown(f"""
    <style>
    body, .stApp {{
        background: {renk['bg']} !important;
    }}
    .themed-card {{
        background: {renk['card']};
        border-radius: 18px;
        padding: 16px;
        margin-top: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 18px 0 {renk['shadow']};
        font-size: 18px;
        color: {renk['text']};
    }}
    .shake {{
        animation: shake 0.7s;
        animation-iteration-count: 1;
        display: inline-block;
    }}
    @keyframes shake {{
      0% {{ transform: rotate(-15deg) scale(1.1); }}
      20% {{ transform: rotate(5deg) scale(1.05); }}
      40% {{ transform: rotate(-8deg) scale(1.08); }}
      60% {{ transform: rotate(4deg) scale(1.03); }}
      80% {{ transform: rotate(-3deg) scale(1.12); }}
      100% {{ transform: rotate(0deg) scale(1); }}
    }}
    .stat-badge {{
        display: inline-block;
        background: {renk['header']};
        color: #fff;
        border-radius: 10px;
        padding: 2px 13px 2px 13px;
        font-weight: 700;
        margin: 0 8px;
        font-size: 17px;
    }}
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(
        f"<h1 class='text-center' style='color:{renk['header']};font-family:QuickAndRegular;'>🎲 Zar Oyunu</h1>",
        unsafe_allow_html=True
    )

    if "zarlar" not in st.session_state:
        st.session_state.zarlar = []
    if "son_zar" not in st.session_state:
        st.session_state.son_zar = 1
    if "anim" not in st.session_state:
        st.session_state.anim = False

    PNG_PATH = ("images")

    def show_dice(num, slot, animate=False):
        img_path = os.path.join(PNG_PATH, f"{num}.png")
        with open(img_path, "rb") as image_file:
            img_bytes = image_file.read()
            encoded = base64.b64encode(img_bytes).decode()
        css_class = "shake" if animate else ""
        slot.markdown(
            f"<div style='display: flex; justify-content: center;'>"
            f"<img src='data:image/png;base64,{encoded}' width='110' class='{css_class}'/>"
            f"</div>", unsafe_allow_html=True
        )

    zar_slot = st.empty()
    show_dice(st.session_state.son_zar, zar_slot, st.session_state.anim)
    st.session_state.anim = False

    colb1, colb2 = st.columns(2)
    if colb1.button("🎲 Zar At", use_container_width=True, key="zar_at"):
        # Animasyon
        for _ in range(18):
            num = random.randint(1, 6)
            show_dice(num, zar_slot, animate=True)
            time.sleep(0.045)
        sonuc = random.randint(1, 6)
        st.session_state.son_zar = sonuc
        show_dice(sonuc, zar_slot, animate=True)
        st.session_state.anim = True
        st.session_state.zarlar.append(sonuc)

    if colb2.button("🔄 Skoru Sıfırla", use_container_width=True, key="reset"):
        st.session_state.zarlar = []
        st.session_state.son_zar = 1
        st.session_state.anim = False
        st.experimental_rerun()

    # Oyuncu için istatistikler
    zarlar = st.session_state.zarlar
    if zarlar:
        minimum = min(zarlar)
        maksimum = max(zarlar)
        ortalama = round(sum(zarlar) / len(zarlar), 2)
        try:
            mod = statistics.mode(zarlar)
        except statistics.StatisticsError:
            mod = zarlar[0]
        st.markdown(f"""
        <div class="themed-card" style="margin-top:0;">
            <span class="stat-badge">Oyuncu</span>
            <b>Atış:</b> {len(zarlar)}
            <b> | Min:</b> {minimum}
            <b> | Max:</b> {maksimum}
            <b> | Mean:</b> {ortalama}
            <b> | Mod:</b> {mod}
            <br>
            <span style="font-size:15px;color:#888;">Tüm Zarlar: {', '.join(str(z) for z in zarlar)}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="themed-card" style="margin-top:0;">
            <span class="stat-badge">Oyuncu</span>
            Hiç zar atmadı.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        f"<div style='text-align: center; color: #999; font-size: 15px; margin-top: 20px;'></div>",
        unsafe_allow_html=True
    )




