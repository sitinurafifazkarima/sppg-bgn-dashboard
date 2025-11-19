# 🚀 Panduan Deployment Dashboard SPPG BGN

## Opsi 1: Streamlit Community Cloud (RECOMMENDED - GRATIS)

### Keuntungan:
- ✅ **100% GRATIS**
- ✅ Deploy dalam 5 menit
- ✅ Automatic updates dari GitHub
- ✅ SSL/HTTPS included
- ✅ Custom domain support
- ✅ No server maintenance

### Langkah-Langkah:

#### 1. Upload ke GitHub

**A. Buat Repository GitHub Baru:**
1. Buka https://github.com
2. Login ke akun GitHub Anda
3. Klik tombol "+" → "New repository"
4. Nama repository: `sppg-bgn-dashboard`
5. Pilih "Public" (required untuk free tier)
6. Klik "Create repository"

**B. Upload File ke GitHub:**

Jalankan command berikut di terminal (PowerShell):

```powershell
cd "d:\MAGANG\INFOMEDIA NUSANTARA\sppg-bgn"

# Initialize git repository
git init

# Add all files
git add dashboard_sppg.py
git add requirements.txt
git add README.md
git add METODOLOGI.md
git add sppg_data_complete_with_coordinates.csv

# Commit
git commit -m "Initial commit: SPPG BGN Dashboard"

# Add remote (ganti YOUR_USERNAME dengan username GitHub Anda)
git remote add origin https://github.com/YOUR_USERNAME/sppg-bgn-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**ATAU Upload Manual via Web:**
1. Buka repository yang baru dibuat
2. Klik "Add file" → "Upload files"
3. Drag & drop semua file yang diperlukan:
   - `dashboard_sppg.py`
   - `requirements.txt`
   - `README.md`
   - `sppg_data_complete_with_coordinates.csv`
4. Klik "Commit changes"

#### 2. Deploy ke Streamlit Cloud

**A. Daftar Streamlit Cloud:**
1. Buka https://share.streamlit.io
2. Klik "Sign up" atau "Continue with GitHub"
3. Authorize Streamlit untuk akses GitHub

**B. Deploy App:**
1. Klik "New app"
2. Pilih repository: `YOUR_USERNAME/sppg-bgn-dashboard`
3. Branch: `main`
4. Main file path: `dashboard_sppg.py`
5. Klik "Deploy!"

**C. Tunggu Deployment:**
- Streamlit akan otomatis install dependencies dari `requirements.txt`
- Proses biasanya 2-5 menit
- Setelah selesai, Anda akan mendapat URL: `https://YOUR_APP_NAME.streamlit.app`

#### 3. Custom Domain (Opsional)

Anda bisa menggunakan custom domain seperti `sppg-bgn.yourdomain.com`:

1. Di Streamlit Cloud dashboard, buka Settings → Custom subdomain
2. Masukkan nama subdomain yang diinginkan
3. Atau gunakan custom domain sendiri dengan setup CNAME record

---

## Opsi 2: Heroku (GRATIS dengan Batasan)

### Keuntungan:
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Support multiple languages

### Langkah-Langkah:

#### 1. Buat File Tambahan

**Procfile:**
```
web: sh setup.sh && streamlit run dashboard_sppg.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

**runtime.txt:**
```
python-3.11.0
```

#### 2. Deploy ke Heroku

```powershell
# Install Heroku CLI
# Download dari: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create sppg-bgn-dashboard

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Opsi 3: Azure Web App (RECOMMENDED untuk CORPORATE)

### Keuntungan:
- ✅ Enterprise-grade security
- ✅ Integration dengan Azure ecosystem
- ✅ High availability
- ✅ Scalable

### Langkah-Langkah:

#### 1. Buat requirements.txt untuk Azure
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0,<2.0.0
gunicorn
```

#### 2. Buat startup.sh
```bash
#!/bin/bash
streamlit run dashboard_sppg.py --server.port=8000 --server.address=0.0.0.0
```

#### 3. Deploy via Azure Portal

1. Login ke https://portal.azure.com
2. Create "Web App"
3. Pilih Python 3.11
4. Upload code via:
   - Azure DevOps
   - GitHub Actions
   - FTP
   - Local Git

---

## Opsi 4: Google Cloud Run

### Keuntungan:
- ✅ Pay per use (sangat murah untuk traffic rendah)
- ✅ Auto-scaling
- ✅ Containerized

### Langkah-Langkah:

#### 1. Buat Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "dashboard_sppg.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

#### 2. Deploy

```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT_ID/sppg-dashboard

# Deploy
gcloud run deploy sppg-dashboard \
  --image gcr.io/PROJECT_ID/sppg-dashboard \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated
```

---

## Opsi 5: Railway.app (GRATIS + MUDAH)

### Keuntungan:
- ✅ Free tier generous
- ✅ Super simple deployment
- ✅ GitHub integration

### Langkah-Langkah:

1. Buka https://railway.app
2. Sign up dengan GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Pilih repository Anda
5. Railway akan auto-detect Streamlit app
6. Deploy otomatis!

URL: `https://YOUR_APP.railway.app`

---

## 📊 Perbandingan Platform

| Platform | Harga | Kemudahan | Speed | Best For |
|----------|-------|-----------|-------|----------|
| **Streamlit Cloud** | ⭐ Gratis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Quick prototype, internal tools |
| **Heroku** | Gratis (limited) | ⭐⭐⭐⭐ | ⭐⭐⭐ | Small projects |
| **Azure** | Bayar | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Enterprise, corporate |
| **Google Cloud Run** | Pay per use | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Scalable apps |
| **Railway** | Gratis + paid | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Quick & easy |

---

## 🔒 Security Considerations

### Untuk Data Sensitif:

1. **Jangan upload data sensitif ke public repository**
   - Gunakan private repository
   - Atau gunakan secrets/environment variables

2. **Authentication:**
   ```python
   import streamlit as st
   
   def check_password():
       def password_entered():
           if st.session_state["password"] == "YOUR_SECURE_PASSWORD":
               st.session_state["password_correct"] = True
           else:
               st.session_state["password_correct"] = False
       
       if "password_correct" not in st.session_state:
           st.text_input("Password", type="password", 
                        on_change=password_entered, key="password")
           return False
       elif not st.session_state["password_correct"]:
           st.text_input("Password", type="password", 
                        on_change=password_entered, key="password")
           st.error("Password incorrect")
           return False
       else:
           return True
   
   if check_password():
       # Your dashboard code here
       main()
   ```

3. **Use Environment Variables untuk konfigurasi:**
   ```python
   import os
   PASSWORD = os.getenv("DASHBOARD_PASSWORD", "default_password")
   ```

---

## 🎯 REKOMENDASI

### Untuk DEMO/INTERNAL TEAM:
➡️ **Streamlit Community Cloud**
- Paling cepat
- Paling mudah
- Gratis
- Perfect untuk showcase

### Untuk PRODUCTION (Internal Company):
➡️ **Azure Web App** atau **Internal Server**
- Kontrol penuh
- Security lebih baik
- Integration dengan infrastruktur existing

### Untuk PUBLIC ACCESS dengan SCALE:
➡️ **Google Cloud Run** atau **AWS ECS**
- Auto-scaling
- Pay per use
- High availability

---

## 📞 Troubleshooting

### Error: "ModuleNotFoundError"
**Solusi:** Pastikan `requirements.txt` lengkap dan ter-update

### Error: "File not found: sppg_data_complete_with_coordinates.csv"
**Solusi:** Pastikan CSV file di-upload ke repository

### App sangat lambat
**Solusi:** 
- Tambahkan `@st.cache_data` decorator
- Optimize data loading
- Gunakan server dengan resource lebih besar

### Authentication tidak berfungsi
**Solusi:** Gunakan Streamlit secrets management atau environment variables

---

## 📝 Checklist Deployment

- [ ] Code ter-upload ke GitHub
- [ ] `requirements.txt` complete dan tested
- [ ] CSV data file included
- [ ] README.md updated
- [ ] App tested locally (`streamlit run dashboard_sppg.py`)
- [ ] Pilih platform deployment
- [ ] Deploy dan test URL
- [ ] Setup custom domain (optional)
- [ ] Add authentication jika perlu
- [ ] Share URL dengan tim

---

## 🎉 Quick Start (5 Menit)

**Cara tercepat deploy:**

1. **Upload ke GitHub** (manual via web)
2. **Buka** https://share.streamlit.io
3. **Sign in** dengan GitHub
4. **New app** → Pilih repository
5. **Deploy!**
6. **Share URL** dengan tim

**DONE!** Dashboard Anda sudah online dan bisa diakses semua orang! 🚀

---

**Need Help?** Contact: [Your Email/Contact]
