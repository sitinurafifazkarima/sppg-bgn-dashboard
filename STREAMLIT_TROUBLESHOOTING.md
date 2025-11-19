# 🔧 Troubleshooting Streamlit Cloud Error

## Error: "Oh no. Error running app"

Ini adalah panduan untuk memperbaiki error di Streamlit Cloud.

---

## ✅ Checklist Cepat

1. **File CSV sudah di-upload ke GitHub?**
   - ✅ Check: Buka https://github.com/sitinurafifazkarima/sppg-bgn-dashboard
   - ✅ Pastikan file `sppg_data_complete_with_coordinates.csv` ada di repository

2. **Repository Public?**
   - ✅ Settings → Danger Zone → Change visibility → Public

3. **Branch benar?**
   - ✅ Di Streamlit Cloud, pastikan branch: `main`

4. **Main file path benar?**
   - ✅ Main file: `dashboard_sppg.py` (bukan `dashboard_sppg_secure.py`)

---

## 🔍 Cara Melihat Error Detail di Streamlit Cloud

1. Buka Streamlit Cloud dashboard: https://share.streamlit.io
2. Klik pada app Anda
3. Klik "Manage app" (kanan atas)
4. Scroll ke bawah ke bagian **"Logs"**
5. Cari error message yang berwarna merah

### Error Umum & Solusi:

#### ❌ Error: "No module named 'plotly'"
**Penyebab:** Dependencies tidak terinstall
**Solusi:** 
- Check `requirements.txt` ada di root repository
- Reboot app: Manage app → Reboot app

#### ❌ Error: "FileNotFoundError: sppg_data_complete_with_coordinates.csv"
**Penyebab:** File CSV tidak ada atau path salah
**Solusi:**
1. Pastikan file CSV di root folder (sama level dengan dashboard_sppg.py)
2. Check di GitHub: https://github.com/sitinurafifazkarima/sppg-bgn-dashboard
3. Jika tidak ada, upload via:
   ```powershell
   cd "d:\MAGANG\INFOMEDIA NUSANTARA\sppg-bgn"
   git add sppg_data_complete_with_coordinates.csv
   git commit -m "Add CSV data file"
   git push
   ```

#### ❌ Error: "Memory limit exceeded"
**Penyebab:** Data terlalu besar untuk free tier
**Solusi:**
1. Reduce data size atau
2. Upgrade ke paid tier atau
3. Use sampling dalam code

#### ❌ Error: "Version conflict" atau "Dependency error"
**Penyebab:** Konflik versi package
**Solusi:** Update `requirements.txt`:
```txt
streamlit>=1.28.0
pandas>=2.0.0,<3.0.0
plotly>=5.17.0
numpy>=1.24.0,<2.0.0
```

---

## 🚀 Quick Fix Steps

### Step 1: Verify Files di GitHub

Buka repository dan pastikan ada:
- ✅ `dashboard_sppg.py`
- ✅ `requirements.txt`
- ✅ `sppg_data_complete_with_coordinates.csv`

### Step 2: Check Streamlit Cloud Settings

1. Buka: https://share.streamlit.io
2. Klik app Anda → "Manage app"
3. Verify:
   - Repository: `sitinurafifazkarima/sppg-bgn-dashboard`
   - Branch: `main`
   - Main file: `dashboard_sppg.py`
   - Python version: `3.11`

### Step 3: Reboot App

Di Streamlit Cloud:
1. Manage app
2. Scroll ke bawah
3. Klik "Reboot app"
4. Tunggu 2-3 menit

### Step 4: Check Logs

Jika masih error, check logs:
1. Manage app
2. Scroll ke "Logs"
3. Copy error message
4. Cari solusi berdasarkan error

---

## 🔧 Fix Spesifik

### Jika CSV File Missing:

```powershell
# Di local machine
cd "d:\MAGANG\INFOMEDIA NUSANTARA\sppg-bgn"

# Pastikan file ada
dir sppg_data_complete_with_coordinates.csv

# Add dan push
git add sppg_data_complete_with_coordinates.csv
git commit -m "Add CSV data file"
git push

# Tunggu 1-2 menit, Streamlit akan auto-redeploy
```

### Jika Dependencies Error:

```powershell
# Update requirements.txt di local
# Edit file requirements.txt

# Push
git add requirements.txt
git commit -m "Update dependencies"
git push

# Di Streamlit Cloud: Reboot app
```

### Jika Memory Error:

Edit `dashboard_sppg.py`, tambahkan sampling:

```python
@st.cache_data
def load_data():
    df = pd.read_csv('sppg_data_complete_with_coordinates.csv')
    
    # For Streamlit Cloud free tier, sample if data too large
    if len(df) > 5000:
        df = df.sample(n=5000, random_state=42)
        st.warning("⚠️ Showing sample of 5000 records (Streamlit Cloud free tier)")
    
    df = df.dropna(subset=['Latitude', 'Longitude'])
    return df
```

---

## 📊 Ukuran File Limits

**Streamlit Cloud Free Tier:**
- Memory: 1GB
- Storage: 1GB
- CPU: Shared

**File size saat ini:**
- CSV: ~750KB ✅ (OK)
- Total repo: Should be < 100MB

---

## 🆘 Masih Error?

### Option 1: Delete & Redeploy

1. Di Streamlit Cloud, delete app
2. Create new app dengan settings yang sama
3. Deploy ulang

### Option 2: Test Locally Dulu

```powershell
cd "d:\MAGANG\INFOMEDIA NUSANTARA\sppg-bgn"
streamlit run dashboard_sppg.py
```

Jika jalan di local, error kemungkinan di Streamlit Cloud settings.

### Option 3: Use Alternative Platform

Jika Streamlit Cloud terus bermasalah:
- Railway.app (lebih mudah)
- Heroku (lebih stabil)
- Deploy di server sendiri

---

## 📞 Get Help

**Streamlit Community:**
- Forum: https://discuss.streamlit.io
- Docs: https://docs.streamlit.io

**GitHub Issues:**
- Create issue di repository

**Quick Contact:**
- Check Streamlit Cloud status: https://status.streamlit.io
- Check GitHub status: https://www.githubstatus.com

---

## ✅ After Fix Checklist

Setelah fix, verify:
- [ ] App loading (tidak ada error message)
- [ ] Map muncul dengan benar
- [ ] Filter di sidebar berfungsi
- [ ] Semua tab (4 tabs) bisa dibuka
- [ ] Data table bisa di-scroll
- [ ] Download button berfungsi

---

## 💡 Prevention Tips

Untuk avoid error di masa depan:

1. **Always test locally** sebelum push:
   ```powershell
   streamlit run dashboard_sppg.py
   ```

2. **Keep requirements.txt minimal:**
   - Hanya package yang benar-benar digunakan
   - Pin major versions

3. **Monitor file sizes:**
   - Keep repo < 100MB
   - Compress large files jika perlu

4. **Use .gitignore:**
   - Exclude unnecessary files
   - Exclude large files that aren't needed

5. **Regular maintenance:**
   - Update packages quarterly
   - Check Streamlit Cloud announcements
   - Keep backup of working version

---

**Last Updated:** Nov 2025
**Status:** ✅ Fixed - Code updated with better error handling

Jika masih ada masalah, check logs di Streamlit Cloud dan share error message!
