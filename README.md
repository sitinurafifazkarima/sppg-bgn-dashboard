# Dashboard SPPG BGN - Analisis Kebutuhan EOS

Dashboard interaktif berbasis Streamlit untuk menganalisis sebaran SPPG (Stasiun Pengamat Pasang Surut dan Gelombang) BGN dan menghitung kebutuhan EOS (Engineering on Site).

## 🎯 Fitur Utama

### 1. **Peta Sebaran SPPG**
- Visualisasi geografis seluruh SPPG di Indonesia
- Filter berdasarkan zona dan wilayah
- Color-coded berdasarkan status operasional
- Distribusi per zona dan wilayah

### 2. **Analisis Kebutuhan EOS**
- Perhitungan otomatis jumlah EOS yang dibutuhkan
- Berdasarkan ratio SPPG to EOS (default: 25:1)
- Adjustment factor untuk sebaran geografis
- Adjustment factor untuk status operasional
- Estimasi perbaikan bulanan

### 3. **Metrik & KPI**
- MTTR (Mean Time to Repair)
- Tingkat utilisasi EOS (target: 60-80%)
- Simulasi dampak MTTR terhadap kebutuhan EOS
- Breakdown status operasional

### 4. **Hierarki Wilayah**
- **Level 1 - Zona:** Regional/Pulau (Jawa, Sumatera, Kalimantan, dll)
- **Level 2 - Wilayah:** Provinsi
- **Level 3 - Area:** Kota/Kabupaten

## 📊 Metodologi Perhitungan EOS

```
EOS Required = (Total SPPG / Ratio) × Spread Factor × Operational Factor

Dimana:
- Ratio: Jumlah SPPG per 1 EOS (default: 25)
- Spread Factor: 1 + (Std Dev Lat + Std Dev Lon) / 10
  * Semakin tersebar geografis = butuh lebih banyak EOS
  * Range: 1.0 - 2.0x
- Operational Factor: 1 + (% SPPG Beroperasi × 0.3)
  * SPPG operasional butuh support lebih aktif
  * Range: 1.0 - 1.3x

Utilization Rate = (Monthly Repairs × MTTR) / (EOS × Working Hours) × 100%
```

## 🚀 Cara Menjalankan

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Jalankan Dashboard

```powershell
streamlit run dashboard_sppg.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`

## 📁 File yang Dibutuhkan

- `dashboard_sppg.py` - Script utama dashboard
- `sppg_data_complete_with_coordinates.csv` - Data SPPG dengan koordinat
- `requirements.txt` - Dependencies Python

## 🎛️ Parameter yang Dapat Disesuaikan

Di sidebar dashboard, Anda dapat menyesuaikan:

1. **Filter Data:**
   - Zona (Regional)
   - Wilayah (Provinsi)
   - Status Operasional

2. **Parameter EOS:**
   - Ratio SPPG per EOS (10-50, default: 25)
   - MTTR - Mean Time to Repair (4-72 jam, default: 24)
   - Hari kerja per bulan (15-30, default: 22)

## 📈 Interpretasi Metrik

### Utilization Rate
- **< 60%**: Kapasitas berlebih, pertimbangkan pengurangan EOS
- **60-80%**: Optimal - sweet spot untuk efisiensi dan responsiveness
- **> 80%**: EOS overworked, risiko burnout dan service delay

### SPPG per EOS
- Target: Sesuai parameter yang diset (default: 25)
- Aktual bisa lebih rendah karena adjustment factors
- Pertimbangkan geografis dan operasional status

### Estimasi Perbaikan Bulanan
- Asumsi failure rate: 5% per bulan
- Hanya menghitung SPPG yang beroperasi
- Digunakan untuk menghitung workload EOS

## 🗺️ Zona Regional

Dashboard menggunakan hierarki zona sebagai berikut:

1. **Zona Jawa**: Banten, DKI Jakarta, Jawa Barat, Jawa Tengah, DIY, Jawa Timur
2. **Zona Sumatera**: Aceh, Sumut, Sumbar, Riau, Kepri, Jambi, Sumsel, Babel, Bengkulu, Lampung
3. **Zona Kalimantan**: Kalbar, Kalteng, Kalsel, Kaltim, Kaltara
4. **Zona Sulawesi**: Sulut, Sulteng, Sulsel, Sultra, Gorontalo, Sulbar
5. **Zona Bali & Nusa Tenggara**: Bali, NTB, NTT
6. **Zona Maluku & Papua**: Maluku, Maluku Utara, Papua, Papua Barat, dan provinsi Papua lainnya

## 💡 Tips Penggunaan

1. **Mulai dengan overview**: Lihat tab "Peta Sebaran" untuk pemahaman umum
2. **Analisis kebutuhan**: Tab "Analisis EOS" untuk planning SDM
3. **Optimasi parameter**: Gunakan tab "Metrik & KPI" untuk fine-tuning
4. **Export data**: Download hasil analisis untuk reporting

## 🔧 Troubleshooting

**Error: File not found**
- Pastikan file `sppg_data_complete_with_coordinates.csv` ada di folder yang sama

**Map tidak muncul**
- Pastikan ada koneksi internet (untuk loading map tiles)
- Check apakah ada data dengan koordinat valid

**Utilisasi rate sangat tinggi/rendah**
- Adjust parameter ratio SPPG per EOS
- Adjust MTTR sesuai kondisi aktual
- Review failure rate assumption (5% di code)

## 📝 Catatan

- Data failure rate (5%) dan parameter lain bisa disesuaikan di code
- Spread factor formula bisa di-tune sesuai kondisi lapangan
- Untuk deployment production, pertimbangkan hosting di Streamlit Cloud atau server internal

## 🤝 Kontribusi

Untuk improvement atau bug report, silakan koordinasi dengan tim development.

---

**Developed for**: Badan Informasi Geospasial (BIG) - BGN SPPG Analysis
**Version**: 1.0.0
**Last Updated**: 2025
