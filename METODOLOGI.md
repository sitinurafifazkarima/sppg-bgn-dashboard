# Dokumentasi Teknis - Dashboard SPPG BGN

## 📐 Metodologi Perhitungan EOS

### 1. Formula Dasar

```python
EOS_Required = ceil(EOS_Dasar × Spread_Factor × Operational_Factor)

Where:
    EOS_Dasar = Total_SPPG / SPPG_per_EOS_Ratio
```

### 2. Spread Factor (Faktor Sebaran Geografis)

**Tujuan:** Mengakomodasi kebutuhan tambahan EOS untuk wilayah dengan sebaran geografis yang luas.

**Formula:**
```python
Spread_Factor = 1 + (Lat_Std + Lon_Std) / 10
Spread_Factor = clip(Spread_Factor, min=1.0, max=2.0)
```

**Interpretasi:**
- `Std` = Standard Deviation dari koordinat Latitude dan Longitude
- Std tinggi = lokasi SPPG lebih tersebar = butuh lebih banyak EOS untuk coverage
- Range: 1.0x (sangat terkonsentrasi) hingga 2.0x (sangat tersebar)

**Contoh:**
- Wilayah dengan 50 SPPG dalam radius 10km: Spread Factor ≈ 1.1x
- Wilayah dengan 50 SPPG tersebar 500km: Spread Factor ≈ 1.8x

### 3. Operational Factor (Faktor Operasional)

**Tujuan:** Memberikan prioritas lebih pada wilayah dengan lebih banyak SPPG yang sudah beroperasi.

**Formula:**
```python
Operational_Factor = 1 + (SPPG_Beroperasi / Total_SPPG) × 0.3
```

**Interpretasi:**
- SPPG yang beroperasi memerlukan maintenance dan support lebih aktif
- SPPG yang belum beroperasi masih dalam tahap setup/konstruksi
- Range: 1.0x (semua belum beroperasi) hingga 1.3x (semua sudah beroperasi)

**Contoh:**
- 100 SPPG, 20 beroperasi: Factor = 1.06x
- 100 SPPG, 80 beroperasi: Factor = 1.24x

### 4. MTTR (Mean Time to Repair)

**Definisi:** Rata-rata waktu yang dibutuhkan untuk menyelesaikan satu perbaikan, dari laporan kerusakan hingga selesai diperbaiki.

**Komponen MTTR:**
```
MTTR = Travel Time + Diagnosis Time + Repair Time + Testing Time

Typical breakdown:
- Travel Time: 2-8 jam (tergantung lokasi)
- Diagnosis: 1-4 jam
- Repair: 2-12 jam
- Testing: 1-2 jam
```

**Impact pada Workload:**
```python
Hours_Needed = Number_of_Repairs × MTTR
```

### 5. Utilization Rate (Tingkat Utilisasi)

**Formula:**
```python
Utilization_Rate = (Monthly_Repairs × MTTR) / (EOS_Count × Working_Hours_per_Month) × 100%

Where:
    Monthly_Repairs = SPPG_Beroperasi × Failure_Rate
    Failure_Rate = 0.05 (5% per bulan - asumsi)
    Working_Hours_per_Month = Working_Days × 8
```

**Target Range:**
- **< 60%**: Under-utilized - Kapasitas berlebih, inefisiensi biaya
- **60-80%**: Optimal - Balance antara efisiensi dan responsiveness
- **> 80%**: Over-utilized - Risiko burnout, delayed response, quality issues

**Interpretasi:**
```
Utilization 50%  → EOS hanya kerja setengah capacity
Utilization 70%  → Sweet spot - masih ada buffer untuk emergency
Utilization 90%  → Red flag - hampir tidak ada waktu untuk preventive maintenance
```

## 🎯 Skenario Penggunaan

### Skenario 1: Planning SDM Baru

**Situasi:** Zona Baru dengan 150 SPPG akan dibuka

**Langkah:**
1. Input data SPPG ke CSV
2. Set ratio SPPG per EOS = 25 (standar)
3. Set MTTR = 24 jam (ekspektasi awal)
4. Lihat hasil: EOS Required

**Hasil Contoh:**
```
Total SPPG: 150
Spread Factor: 1.5x (cukup tersebar)
Operational Factor: 1.1x (30% sudah beroperasi)
EOS Required: ceil(150/25 × 1.5 × 1.1) = 10 EOS
```

### Skenario 2: Evaluasi Kapasitas Existing

**Situasi:** Zona sudah ada 8 EOS, menangani 180 SPPG. Apakah cukup?

**Analisis:**
```
Utilisasi saat ini: 85% → Over-utilized!
Rekomendasi: Tambah 2-3 EOS untuk turunkan ke 65-70%
```

### Skenario 3: Optimasi Biaya

**Situasi:** Budget cut, perlu reduce EOS dari 15 ke 12

**Impact Analysis:**
```
Sebelum: 15 EOS → Utilisasi 65% (optimal)
Sesudah: 12 EOS → Utilisasi 81% (borderline)

Risk:
- Response time naik 20-30%
- Preventive maintenance berkurang
- Risiko backlog saat peak season
```

## 📊 Asumsi & Konstanta

### Default Values

```python
SPPG_PER_EOS_RATIO = 25         # 1 EOS untuk 25 SPPG
MTTR_HOURS = 24                  # 24 jam rata-rata repair
WORKING_DAYS_PER_MONTH = 22      # 22 hari kerja
WORKING_HOURS_PER_DAY = 8        # 8 jam per hari
FAILURE_RATE = 0.05              # 5% SPPG mengalami issue per bulan
SPREAD_FACTOR_DIVISOR = 10       # Untuk normalisasi std dev
SPREAD_FACTOR_MAX = 2.0          # Max multiplier untuk sebaran
OPERATIONAL_MULTIPLIER = 0.3     # Weight untuk operational status
```

### Asumsi Failure Rate

**5% per bulan** berdasarkan:
- Hardware failure: 2%
- Network issues: 1.5%
- Power/environmental: 1%
- Software/calibration: 0.5%

**Penyesuaian:**
- Area coastal/harsh: +1-2%
- Brand new equipment: -1-2%
- Aging infrastructure (>10 tahun): +2-3%

## 🔄 Kalibrasi & Tuning

### Cara Kalibrasi Parameter

1. **Kumpulkan Data Historis** (minimal 6 bulan):
   - Jumlah repair calls per bulan
   - Rata-rata waktu penyelesaian (actual MTTR)
   - Jumlah EOS dan SPPG
   - Workload per EOS

2. **Hitung Actual Metrics:**
   ```python
   Actual_Utilization = Total_Repair_Hours / (EOS × Working_Hours)
   Actual_MTTR = Total_Repair_Hours / Number_of_Repairs
   Actual_Failure_Rate = Number_of_Repairs / SPPG_Beroperasi
   ```

3. **Adjust Formula:**
   - Jika Actual > Predicted: Naikkan failure rate atau MTTR
   - Jika Actual < Predicted: Turunkan parameter

### Red Flags untuk Review

- Utilisasi consistently > 85%
- MTTR trend meningkat (equipment aging)
- Failure rate > 10% (perlu investigasi root cause)
- Spread factor tidak mencerminkan travel time actual

## 💡 Best Practices

### Untuk Planning:
1. ✅ Gunakan data historis untuk kalibrasi
2. ✅ Review parameter setiap 6 bulan
3. ✅ Buffer 10-15% untuk growth dan unexpected
4. ✅ Pertimbangkan seasonal variation
5. ✅ Include travel time dalam MTTR calculation

### Untuk Operation:
1. ✅ Track actual MTTR per wilayah
2. ✅ Monitor utilisasi real-time
3. ✅ Alert jika utilisasi > 80% sustained
4. ✅ Preventive maintenance schedule
5. ✅ Cross-training EOS untuk flexibility

### Untuk Reporting:
1. ✅ Monthly KPI dashboard
2. ✅ Quarterly capacity review
3. ✅ Annual strategic planning
4. ✅ Benchmark antar zona
5. ✅ ROI analysis per EOS

## 📈 Future Enhancements

### Potential Improvements:

1. **Machine Learning Prediction:**
   - Predict failure patterns
   - Optimize EOS routing
   - Seasonal demand forecasting

2. **Real-time Integration:**
   - Live SPPG status monitoring
   - Dynamic workload allocation
   - GPS tracking untuk travel time actual

3. **Advanced Analytics:**
   - Heat map untuk high-failure areas
   - Equipment lifespan analysis
   - Predictive maintenance scheduling

4. **Optimization Algorithms:**
   - Optimal EOS placement
   - Territory balancing
   - Resource allocation optimization

## 📞 Support & Feedback

Untuk pertanyaan teknis atau request enhancement:
- Review kode di `dashboard_sppg.py`
- Adjust constants di bagian `calculate_eos_requirements()`
- Modify zona mapping di `create_zones()`

---

**Document Version:** 1.0
**Last Updated:** November 2025
**Author:** Data Analytics Team
