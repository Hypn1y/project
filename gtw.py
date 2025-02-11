import streamlit as st
import pandas as pd
import cv2
import os
import numpy as np
from datetime import datetime

# Direktori untuk menyimpan foto
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

# File CSV untuk menyimpan data tamu
DATA_FILE = "buku_tamu.csv"

# Fungsi untuk menyimpan data ke CSV
def save_to_csv(data):
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame([data])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# Tampilan di Streamlit
st.title("📖 Buku Tamu Digital")

# Form Input
nama = st.text_input("Nama", placeholder="Masukkan nama lengkap Anda")
instansi = st.text_input("Instansi/Jabatan", placeholder="Masukkan instansi atau jabatan Anda")
keperluan = st.text_area("Keperluan", placeholder="Tulis keperluan kunjungan Anda")

# Kamera untuk menangkap foto
image_file = st.camera_input("Ambil Foto Wajah Anda")

# Tombol Kirim
if st.button("Kirim"):
    if nama and instansi and keperluan and image_file:
        img = cv2.imdecode(np.frombuffer(image_file.getvalue(), np.uint8), 1)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_filename = f"{nama.replace(' ', '_')}_{timestamp}.jpg"
        photo_path = os.path.join(PHOTO_DIR, photo_filename)

        # Simpan gambar
        cv2.imwrite(photo_path, img)

        # Simpan data ke CSV
        new_entry = {
            "Nama": nama,
            "Instansi": instansi,
            "Keperluan": keperluan,
            "Foto": photo_path,
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_to_csv(new_entry)

        st.success(f"Terima kasih, {nama}! Data Anda telah disimpan.")
        st.image(img, caption="Foto Wajah Anda", use_container_width=True)

    else:
        st.error("Semua kolom dan foto wajib diisi!")
