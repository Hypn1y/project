import streamlit as st
import numpy as np
import scipy.integrate as spi

# Konstanta gravitasi
G = 6.674 * 10**-11  # m^3/kg/s^2

st.title("Kalkulator Gravitasi Berdasarkan Kedalaman")

#st.write("""
#Aplikasi ini menghitung percepatan gravitasi berdasarkan kedalaman dan densitas lapisan bumi.
#Silakan masukkan data kedalaman dan densitas atau gunakan nilai default.
#""")

# Dataset otomatis untuk kedalaman dan densitas (hingga 50 km)
default_kedalaman = " "
default_densitas = " "

# Input dari pengguna
kedalaman_input = st.text_area("Masukkan kedalaman (meter, pisahkan dengan koma):", default_kedalaman)
densitas_input = st.text_area("Masukkan densitas (kg/m³, pisahkan dengan koma):", default_densitas)

if st.button("Hitung Gravitasi"):
    try:
        # Konversi input ke array numerik
        kedalaman = np.array([float(x.strip()) for x in kedalaman_input.split(",")])
        densitas = np.array([float(x.strip()) for x in densitas_input.split(",")])

        if len(kedalaman) != len(densitas):
            st.error("Jumlah data kedalaman dan densitas harus sama!")
        else:
            # Fungsi untuk menghitung gravitasi
            def hitung_gravitasi(kedalaman, densitas):
                g = []
                for i in range(len(kedalaman)):
                    integral, _ = spi.quad(lambda z: 4 * np.pi * G * np.interp(z, kedalaman, densitas), 0, kedalaman[i])
                    g.append(integral)
                return np.array(g)

            gravitasi = hitung_gravitasi(kedalaman, densitas)

            # Tampilkan hasil
            st.subheader("Hasil Perhitungan")
            for d, g in zip(kedalaman, gravitasi):
                st.write(f"*Kedalaman: {d} m* → Gravitasi: {g:.6e} m/s²")

    except ValueError:
        st.error("Pastikan hanya memasukkan angka yang dipisahkan dengan koma!")
