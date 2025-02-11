import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# Folder penyimpanan
DATA_FOLDER = "guestbook_data"
IMG_FOLDER = os.path.join(DATA_FOLDER, "images")
CSV_FILE = os.path.join(DATA_FOLDER, "guestbook.csv")

# Pastikan folder ada
os.makedirs(IMG_FOLDER, exist_ok=True)

# Load atau buat data
if os.path.exists(CSV_FILE):
    guestbook_df = pd.read_csv(CSV_FILE)
else:
    guestbook_df = pd.DataFrame(columns=["Nama", "Waktu", "Foto"])

st.title("Buku Tamu")

# Form input
nama = st.text_input("Nama:")
ambil_foto = st.button("Ambil Foto")

if ambil_foto and nama:
    # Ambil gambar dari webcam
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nama}.jpg"
        filepath = os.path.join(IMG_FOLDER, filename)
        cv2.imwrite(filepath, frame)
        cam.release()
        st.image(frame, caption="Foto Anda", use_column_width=True)
        
        # Simpan ke CSV
        new_entry = pd.DataFrame([[nama, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), filename]], columns=["Nama", "Waktu", "Foto"])
        guestbook_df = pd.concat([guestbook_df, new_entry], ignore_index=True)
        guestbook_df.to_csv(CSV_FILE, index=False)
        st.success("Data berhasil disimpan!")
    else:
        st.error("Gagal mengambil gambar")
    cam.release()

# Tampilkan daftar tamu
st.subheader("Daftar Tamu")
if not guestbook_df.empty:
    for _, row in guestbook_df.iterrows():
        st.write(f"**{row['Nama']}** - {row['Waktu']}")
        img_path = os.path.join(IMG_FOLDER, row['Foto'])
        if os.path.exists(img_path):
            st.image(Image.open(img_path), caption=row['Nama'], use_column_width=True)
else:
    st.write("Belum ada tamu yang mengisi.")
