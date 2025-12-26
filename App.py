import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURASI SYSTEM (UI SOLO LEVELING) ---
st.set_page_config(page_title="SYSTEM: Daily Quest", page_icon="⚔️", layout="centered")

# CSS Custom untuk nuansa "System Window" Solo Leveling (Biru Neon & Gelap)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00ffea;
    }
    h1 {
        text-shadow: 0 0 10px #00ffea;
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stCheckbox label {
        color: #ffffff !important;
        font-size: 20px !important;
    }
    .stProgress > div > div > div > div {
        background-color: #00ffea;
    }
    .big-font {
        font-size:20px !important;
        color: #c4c4c4;
    }
    .alert-box {
        border: 2px solid #00ffea;
        padding: 10px;
        border-radius: 5px;
        background-color: rgba(0, 255, 234, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI KEAMANAN (LOGIN) ---
def check_password():
    """Hanya Player terpilih yang bisa akses."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.markdown("# 🔒 SYSTEM ACCESS LOCKED")
        password = st.text_input("Enter Player Key:", type="password")
        # Ganti 'sungjinwoo' dengan password keinginanmu
        if password == "sungjinwoo": 
            st.session_state.password_correct = True
            st.rerun()
        elif password:
            st.error("ACCESS DENIED. You are not the Player.")
        return False
    return True

# --- LOGIKA UTAMA ---
if check_password():
    # Judul System
    st.markdown("# ⚔️ DAILY QUEST: PREPARATION")
    st.markdown("<div class='big-font'>Goal: Become the Shadow Monarch</div>", unsafe_allow_html=True)
    st.write("---")

    # 1. KONEKSI KE GOOGLE SHEETS
    # Ini akan membuat aplikasi membaca data dari sheet kamu
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Ambil data yang ada
    try:
        data = conn.read(worksheet="Sheet1", usecols=list(range(5)), ttl=5)
        data = data.dropna(how="all")
    except:
        # Kalau sheet kosong/baru, buat struktur awal
        data = pd.DataFrame(columns=["date", "push_up", "sit_up", "squat", "lari"])

    # 2. CEK TANGGAL HARI INI
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Cek apakah hari ini sudah ada datanya di database?
    if data.empty or today not in data["date"].values:
        # Kalau belum ada (hari baru), buat baris baru dengan status False (belum dikerjakan)
        new_row = pd.DataFrame([{
            "date": today,
            "push_up": False,
            "sit_up": False,
            "squat": False,
            "lari": False
        }])
        data = pd.concat([data, new_row], ignore_index=True)
        # Update ke Google Sheets
        conn.update(worksheet="Sheet1", data=data)

    # Ambil index data hari ini
    today_index = data[data["date"] == today].index[0]

    # 3. TAMPILAN CHECKLIST (QUEST)
    st.markdown(f"### 📅 DATE: {today}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Checkbox Push-up
        push_up = st.checkbox("Push-up: 100", value=bool(data.at[today_index, "push_up"]))
        if push_up != data.at[today_index, "push_up"]:
            data.at[today_index, "push_up"] = push_up
            conn.update(worksheet="Sheet1", data=data)
            st.rerun()

        # Checkbox Sit-up
        sit_up = st.checkbox("Sit-up: 100", value=bool(data.at[today_index, "sit_up"]))
        if sit_up != data.at[today_index, "sit_up"]:
            data.at[today_index, "sit_up"] = sit_up
            conn.update(worksheet="Sheet1", data=data)
            st.rerun()

    with col2:
        # Checkbox Squat
        squat = st.checkbox("Squat: 100", value=bool(data.at[today_index, "squat"]))
        if squat != data.at[today_index, "squat"]:
            data.at[today_index, "squat"] = squat
            conn.update(worksheet="Sheet1", data=data)
            st.rerun()

        # Checkbox Lari
        lari = st.checkbox("Running: 10km", value=bool(data.at[today_index, "lari"]))
        if lari != data.at[today_index, "lari"]:
            data.at[today_index, "lari"] = lari
            conn.update(worksheet="Sheet1", data=data)
            st.rerun()

    # 4. HITUNG PROGRES
    tasks = [push_up, sit_up, squat, lari]
    completed_count = sum(tasks)
    total_tasks = len(tasks)
    progress = completed_count / total_tasks

    st.write("---")
    st.write(f"Quest Completion: {int(progress * 100)}%")
    st.progress(progress)

    # 5. REWARD SYSTEM
    if progress == 1.0:
        st.markdown("""
            <div class='alert-box'>
            <h3>🎉 QUEST COMPLETED</h3>
            <p>Reward: Status Recovery Approved.</p>
            <p>You have become stronger today.</p>
            </div>
        """, unsafe_allow_html=True)
        st.balloons()
    elif progress == 0:
        st.caption("WARNING: Failure to complete daily quest will result in penalty zone.")