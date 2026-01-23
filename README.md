**EZ EXAM GRADER**

##Tentang Proyek Ini

Aplikasi koreksi ujian berbasis komputer (PC) yang dirancang untuk mengotomatisasi proses penilaian lembar jawaban siswa. Aplikasi ini dibuat dengan Python dan menerapkan prinsip desain SOLID, sehingga menghasilkan program yang fleksibel dan mudah dikembangkan untuk menangani berbagai format ujian.

Untuk saat ini (tahap demo/ mock), sistem ini bekerja menggunakan data terstruktur berformat JSON. Data JSON ini sebagai simulasi dari data yang nantinya akan dihasilkan oleh mesin OMR (Optical Mark Recognition) dan OCR. Dengan begini, kami bisa melakukan pengujian menyeluruh terhadap logika penilaian, kemampuan membuat laporan, dan alur kerja aplikasi secara keseluruhan.

**Project Members (Sukuna Survivors):**
- Grace Putri Wijaya (211110121)
- Rio Frederich (211112075)

**Fitur-Fitur Utama**

- Sistem Koreksi Modular: Bisa menilai berbagai tipe soal (Pilihan Ganda, Isian Singkat, Esai) berkat desain yang pluggable (bisa dicabut-pasang). Tipe soal baru bisa ditambahkan tanpa perlu mengubah mesin koreksi utamanya.

- Penilaian Berbasis Poin: Setiap soal di kunci jawaban bisa diberi poin yang berbeda-beda, jadi pembobotan nilai ujian bisa diatur dengan fleksibel.

- Koreksi Esai Manual: Untuk soal subjektif seperti esai, aplikasi akan menampilkan jawaban siswa dan meminta guru untuk memasukkan nilai secara manual. Nilai ini akan otomatis digabungkan ke dalam nilai akhir.

- Laporan Otomatis: Program akan otomatis membuat laporan nilai lengkap untuk kelas dalam format .xlsx (Excel), yang berisi nama siswa, kelas, dan skor akhir mereka.

- Alur Kerja Berbasis File: Semua data ujian, termasuk kunci jawaban dan jawaban siswa, diambil dari file JSON eksternal. Ini memisahkan antara logika program dan datanya.


**Struktur Proyek**
├── exam_grader/ # Aplikasi utama
│ ├── app.py # Orchestrator Aplikasi utama
│ ├── grading/ # Semua logika grading disini (Grader, GradingTypes)
│ ├── models.py # Model Data (StudentResult, AnswerKey)
│ ├── processing/ # (Utk UAS nanti: ditaruh logika OCR/OMR)
│ ├── reporting/ # Generator laporan (Excel, PDF(UAS))
│ └── utils/ # Utility (UI, FileManager)
│
├── input_data/ # Sampel/ Mock Data sesuai dengan Mapel
│ ├── answer_keys/ 
│ └── student_answers/ 
│
├── output/ # Semua laporan excel dan pdf disini
├── main.py 
└── README.md 