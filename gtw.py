import cv2
import pandas as pd
import os
import streamlit as st
from datetime import datetime

# Folder untuk menyimpan foto dan file CSV
PHOTO_DIR = "photos"
DATA_FILE = "buku_tamu.csv"
os.makedirs(PHOTO_DIR, exist_ok=True)

# Fungsi untuk menyimpan data tamu ke CSV
def save_to_csv(data):
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame([data])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# Fungsi untuk mengambil gambar dari kamera eksternal
def capture_image():
    cap = cv2.VideoCapture(0)  # 0 untuk kamera utama, ubah ke 1 jika menggunakan kamera eksternal
    if not cap.isOpened():
        print("Gagal membuka kamera!")
        return None
    
    print("Tekan 'Space' untuk mengambil gambar, 'Esc' untuk keluar")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal menangkap gambar!")
            break
        
        cv2.imshow("Tekan Space untuk mengambil gambar", frame)
        key = cv2.waitKey(1)
        if key == 32:  # Tombol Space untuk menangkap gambar
            cap.release()
            cv2.destroyAllWindows()
            return frame
        elif key == 27:  # Tombol Esc untuk keluar
            cap.release()
            cv2.destroyAllWindows()
            return None
    
    cap.release()
    cv2.destroyAllWindows()
    return None

# Input data tamu
nama = input("Masukkan Nama: ")
instansi = input("Masukkan Instansi/Jabatan: ")
keperluan = input("Masukkan Keperluan: ")

# Ambil gambar dari kamera
image = capture_image()
if image is not None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_filename = f"{nama.replace(' ', '_')}_{timestamp}.jpg"
    photo_path = os.path.join(PHOTO_DIR, photo_filename)
    cv2.imwrite(photo_path, image)
    print(f"Foto tersimpan di: {photo_path}")

    # Simpan data ke CSV
    new_entry = {
        "Nama": nama,
        "Instansi": instansi,
        "Keperluan": keperluan,
        "Foto": photo_path,
        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_to_csv(new_entry)
    print("Data tamu berhasil disimpan!")
else:
    print("Gagal mengambil foto, data tidak disimpan.")
