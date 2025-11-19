"""
Script untuk memperbaiki format koordinat di CSV
"""
import pandas as pd
import numpy as np

print("🔍 Membaca file CSV...")
df = pd.read_csv('sppg_data_complete_with_coordinates.csv')

print(f"✅ Total records: {len(df)}")
print(f"📊 Columns: {df.columns.tolist()}")

# Check original data
print("\n" + "="*60)
print("📍 ANALISIS KOORDINAT ORIGINAL")
print("="*60)

print(f"\nLatitude:")
print(f"  - Type: {df['Latitude'].dtype}")
print(f"  - Min: {df['Latitude'].min()}")
print(f"  - Max: {df['Latitude'].max()}")
print(f"  - Missing: {df['Latitude'].isna().sum()}")
print(f"  - Non-numeric: {pd.to_numeric(df['Latitude'], errors='coerce').isna().sum()}")

print(f"\nLongitude:")
print(f"  - Type: {df['Longitude'].dtype}")
print(f"  - Min: {df['Longitude'].min()}")
print(f"  - Max: {df['Longitude'].max()}")
print(f"  - Missing: {df['Longitude'].isna().sum()}")
print(f"  - Non-numeric: {pd.to_numeric(df['Longitude'], errors='coerce').isna().sum()}")

# Indonesia coordinate ranges:
# Latitude: -11° to 6° (South to North)
# Longitude: 95° to 141° (West to East)

print("\n" + "="*60)
print("🔧 VALIDASI & PERBAIKAN")
print("="*60)

# Create backup
print("\n1. Membuat backup original...")
df_original = df.copy()

# Convert to numeric (force any string to NaN)
print("2. Convert to numeric...")
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

# Check for out of range coordinates
print("3. Check koordinat di luar Indonesia...")
invalid_lat = (df['Latitude'] < -11) | (df['Latitude'] > 6)
invalid_lon = (df['Longitude'] < 95) | (df['Longitude'] > 141)

print(f"   - Latitude di luar range Indonesia: {invalid_lat.sum()}")
print(f"   - Longitude di luar range Indonesia: {invalid_lon.sum()}")

if invalid_lat.sum() > 0:
    print("\n   ❌ Koordinat Latitude invalid:")
    print(df[invalid_lat][['ID_SPPG', 'Provinsi', 'Kota_Kabupaten', 'Latitude', 'Longitude']].head(10))

if invalid_lon.sum() > 0:
    print("\n   ❌ Koordinat Longitude invalid:")
    print(df[invalid_lon][['ID_SPPG', 'Provinsi', 'Kota_Kabupaten', 'Latitude', 'Longitude']].head(10))

# Check for coordinates = 0
print("\n4. Check koordinat = 0...")
zero_coords = (df['Latitude'] == 0) | (df['Longitude'] == 0)
print(f"   - Records dengan koordinat 0: {zero_coords.sum()}")

# Fix: Set invalid coordinates to NaN
print("\n5. Set koordinat invalid menjadi NaN...")
df.loc[invalid_lat, 'Latitude'] = np.nan
df.loc[invalid_lon, 'Longitude'] = np.nan
df.loc[zero_coords, ['Latitude', 'Longitude']] = np.nan

# Round coordinates to 6 decimal places (precision ~10cm)
print("6. Round koordinat ke 6 desimal...")
df['Latitude'] = df['Latitude'].round(6)
df['Longitude'] = df['Longitude'].round(6)

# Remove duplicate coordinates (keep first)
print("7. Remove duplicate koordinat...")
before_dup = len(df)
df_no_dup = df.drop_duplicates(subset=['Latitude', 'Longitude'], keep='first')
duplicates_removed = before_dup - len(df_no_dup)
print(f"   - Duplicates removed: {duplicates_removed}")

# Statistics after cleaning
print("\n" + "="*60)
print("📊 HASIL SETELAH CLEANING")
print("="*60)

print(f"\nTotal records: {len(df)}")
print(f"Records dengan koordinat valid: {df.dropna(subset=['Latitude', 'Longitude']).shape[0]}")
print(f"Records dengan koordinat missing: {df[df['Latitude'].isna() | df['Longitude'].isna()].shape[0]}")

print(f"\nLatitude (cleaned):")
print(f"  - Min: {df['Latitude'].min()}")
print(f"  - Max: {df['Latitude'].max()}")
print(f"  - Mean: {df['Latitude'].mean():.6f}")

print(f"\nLongitude (cleaned):")
print(f"  - Min: {df['Longitude'].min()}")
print(f"  - Max: {df['Longitude'].max()}")
print(f"  - Mean: {df['Longitude'].mean():.6f}")

# Distribution by province
print("\n" + "="*60)
print("📍 DISTRIBUSI PER PROVINSI (Top 10)")
print("="*60)
valid_coords = df.dropna(subset=['Latitude', 'Longitude'])
prov_dist = valid_coords['Provinsi'].value_counts().head(10)
for prov, count in prov_dist.items():
    print(f"  {prov}: {count}")

# Save cleaned data
print("\n" + "="*60)
print("💾 MENYIMPAN DATA")
print("="*60)

# Save with valid coordinates only
df_valid = df.dropna(subset=['Latitude', 'Longitude'])
output_file = 'sppg_data_complete_with_coordinates.csv'
output_file_valid = 'sppg_data_valid_coordinates.csv'

print(f"\n1. Menyimpan semua data (termasuk yang koordinat kosong)...")
df.to_csv(output_file, index=False)
print(f"   ✅ Saved: {output_file} ({len(df)} records)")

print(f"\n2. Menyimpan hanya data dengan koordinat valid...")
df_valid.to_csv(output_file_valid, index=False)
print(f"   ✅ Saved: {output_file_valid} ({len(df_valid)} records)")

# Summary
print("\n" + "="*60)
print("✅ SUMMARY")
print("="*60)
print(f"""
Original records: {len(df_original)}
Final records (all): {len(df)}
Final records (valid coords): {len(df_valid)}
Records removed: {len(df_original) - len(df)}
Duplicate coords removed: {duplicates_removed}

Files created:
  1. {output_file} - All data (dengan NaN untuk koordinat invalid)
  2. {output_file_valid} - Only valid coordinates

Coordinate format:
  - Precision: 6 decimal places (~10cm accuracy)
  - Latitude range: -11° to 6° (Indonesia)
  - Longitude range: 95° to 141° (Indonesia)
""")

print("\n✅ SELESAI! Data koordinat sudah diperbaiki.")
print("\nUntuk dashboard Streamlit, gunakan salah satu file:")
print(f"  - {output_file_valid} (recommended - hanya koordinat valid)")
print(f"  - {output_file} (include all, dashboard akan filter NaN)")
