import pandas as pd
import numpy as np

# Bikin data 500 mahasiswa PPKU
np.random.seed(42)
n_students = 500

data = {
    'ID_Mahasiswa': [f'M{str(i).zfill(4)}' for i in range(1, n_students + 1)],
    'Jalur_Masuk': np.random.choice(['SNBP', 'SNBT', 'Mandiri'], n_students, p=[0.3, 0.4, 0.3]),
    'Nilai_Matematika': np.random.normal(75, 10, n_students).clip(40, 100).astype(int),
    'Nilai_Biologi': np.random.normal(80, 8, n_students).clip(40, 100).astype(int),
    'Nilai_Fisika': np.random.normal(65, 12, n_students).clip(30, 100).astype(int),
    'Nilai_Kimia': np.random.normal(70, 11, n_students).clip(35, 100).astype(int),
    'Nilai_B_Inggris': np.random.normal(82, 7, n_students).clip(50, 100).astype(int),
    'Tingkat_Kehadiran': np.random.normal(90, 8, n_students).clip(50, 100).astype(int),
}

df = pd.DataFrame(data)

# Hitung Rata-rata
df['Rata_Rata'] = df[['Nilai_Matematika', 'Nilai_Biologi', 'Nilai_Fisika', 'Nilai_Kimia', 'Nilai_B_Inggris']].mean(axis=1).round(2)

# Tentukan Status Akademik (Aman vs Butuh Evaluasi)
# Syarat aman: Rata-rata >= 65 DAN Kehadiran >= 80
df['Status_Akademik'] = np.where((df['Rata_Rata'] >= 65) & (df['Tingkat_Kehadiran'] >= 80), 'Aman', 'Butuh Evaluasi')

# Save ke CSV
df.to_csv('data_akademik_dummy.csv', index=False)
print("Dataset berhasil dibuat: data_akademik_dummy.csv 📊")