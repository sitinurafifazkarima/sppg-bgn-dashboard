# 🚀 Quick Deploy ke Streamlit Cloud

## Cara Tercepat (5 Menit)

### Step 1: Upload ke GitHub

#### Opsi A: Via Git Command (Recommended)

```powershell
# 1. Initialize git
cd "d:\MAGANG\INFOMEDIA NUSANTARA\sppg-bgn"
git init

# 2. Add files
git add .

# 3. Commit
git commit -m "Initial commit: SPPG BGN Dashboard"

# 4. Create repository di GitHub.com:
#    - Buka https://github.com/new
#    - Repository name: sppg-bgn-dashboard
#    - Pilih: Public
#    - JANGAN centang "Initialize with README"
#    - Klik "Create repository"

# 5. Add remote dan push (ganti YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/sppg-bgn-dashboard.git
git branch -M main
git push -u origin main
```

#### Opsi B: Upload Manual (Lebih Mudah)

1. **Buat Repository:**
   - Buka https://github.com/new
   - Nama: `sppg-bgn-dashboard`
   - Public
   - Klik "Create repository"

2. **Upload Files:**
   - Klik "uploading an existing file"
   - Drag & drop SEMUA file dari folder ini
   - Files yang wajib:
     - ✅ `dashboard_sppg.py`
     - ✅ `requirements.txt`
     - ✅ `sppg_data_complete_with_coordinates.csv`
     - ✅ `README.md`
   - Files opsional:
     - `METODOLOGI.md`
     - `DEPLOYMENT_GUIDE.md`
     - `.streamlit/config.toml`
   - Klik "Commit changes"

### Step 2: Deploy ke Streamlit Cloud

1. **Buka Streamlit Cloud:**
   - https://share.streamlit.io
   
2. **Sign In:**
   - Klik "Continue with GitHub"
   - Authorize Streamlit

3. **Deploy App:**
   - Klik "New app"
   - Repository: `YOUR_USERNAME/sppg-bgn-dashboard`
   - Branch: `main`
   - Main file path: `dashboard_sppg.py`
   - Klik "Deploy!"

4. **Tunggu:**
   - Deployment biasanya 2-5 menit
   - Anda akan dapat URL: `https://YOUR-APP-NAME.streamlit.app`

### Step 3: Share!

**Dashboard Anda sudah ONLINE!** 🎉

Share URL dengan siapa saja:
```
https://YOUR-APP-NAME.streamlit.app
```

---

## 🔒 Jika Ingin Menambahkan Password

Gunakan `dashboard_sppg_secure.py` sebagai main file:

1. Di Streamlit Cloud settings, ubah:
   - Main file: `dashboard_sppg_secure.py`

2. Default credentials:
   - Username: `admin`
   - Password: `admin123`

3. **PENTING:** Ganti password di file `auth.py` sebelum deploy!

---

## ⚡ Update Dashboard

Setiap kali Anda push perubahan ke GitHub, Streamlit Cloud akan otomatis update!

```powershell
git add .
git commit -m "Update dashboard"
git push
```

---

## 📱 Akses Dashboard

Setelah deploy berhasil, dashboard bisa diakses:

- ✅ **Desktop**: Browser biasa
- ✅ **Mobile**: Responsive, bisa dibuka di HP
- ✅ **Tablet**: Optimal viewing
- ✅ **Share**: Kirim link ke siapa saja

---

## 🆘 Troubleshooting

### "Repository not found"
- Pastikan repository di GitHub adalah **Public**

### "ModuleNotFoundError"
- Check `requirements.txt` sudah ter-upload
- Pastikan semua dependencies tercantum

### "File not found: CSV"
- Pastikan `sppg_data_complete_with_coordinates.csv` ter-upload ke GitHub

### App tidak load
- Check logs di Streamlit Cloud dashboard
- Pastikan tidak ada error di `dashboard_sppg.py`

---

## 📞 Need Help?

1. Check Streamlit Docs: https://docs.streamlit.io
2. Community Forum: https://discuss.streamlit.io
3. GitHub Issues: Create issue di repository Anda

---

**Happy Deploying!** 🚀
