import abc

class DokumenAkademik(abc.ABC):
    def __init__(self, nama_siswa, id_siswa):
        self._nama_siswa = nama_siswa
        self._id_siswa = id_siswa
        self._nilai = 0

    def get_info_siswa(self):
        return f"Nama: {self._nama_siswa}, ID: {self._id_siswa}"

    def set_nilai(self, nilai):
        if 0 <= nilai <= 100:
            self._nilai = nilai
        else:
            print("Error: Nilai harus di antara 0 dan 100.")

    def get_nilai(self):
        return self._nilai

    @abc.abstractmethod
    def proses_penilaian(self):
        pass


class UjianPilihanGanda(DokumenAkademik):
    def __init__(self, nama_siswa, id_siswa, kunci_jawaban):
        super().__init__(nama_siswa, id_siswa)
        self._kunci_jawaban = kunci_jawaban

    def proses_penilaian(self):
        print(f"\nMenilai Ujian Pilihan Ganda untuk {self._nama_siswa}")
        jawaban_siswa = input(f"Masukkan jawaban siswa ({len(self._kunci_jawaban)} soal): ").upper()
        
        skor = 0
        for i in range(len(self._kunci_jawaban)):
            if i < len(jawaban_siswa) and jawaban_siswa[i] == self._kunci_jawaban[i]:
                skor += 1
        
        nilai_akhir = (skor / len(self._kunci_jawaban)) * 100
        self.set_nilai(nilai_akhir)
        print(f"Hasil: {skor} dari {len(self._kunci_jawaban)} benar. Nilai Akhir: {self.get_nilai():.2f}")


class TugasEsai(DokumenAkademik):
    def __init__(self, nama_siswa, id_siswa):
        super().__init__(nama_siswa, id_siswa)

    def proses_penilaian(self):
        print(f"\nMenilai Tugas Esai untuk {self._nama_siswa}")
        while True:
            try:
                nilai_struktur = float(input("Masukkan nilai struktur (0-100): "))
                nilai_konten = float(input("Masukkan nilai konten (0-100): "))
                if not (0 <= nilai_struktur <= 100 and 0 <= nilai_konten <= 100):
                    raise ValueError("Nilai harus di antara 0 dan 100.")
                break
            except ValueError as e:
                print(f"Input tidak valid: {e}. Silakan coba lagi.")

        nilai_akhir = (nilai_struktur * 0.4) + (nilai_konten * 0.6)
        self.set_nilai(nilai_akhir)
        print(f"Nilai Esai Akhir: {self.get_nilai():.2f}")


class ProyekPemrograman(DokumenAkademik):
    def __init__(self, nama_siswa, id_siswa):
        super().__init__(nama_siswa, id_siswa)

    def proses_penilaian(self):
        print(f"\nMenilai Proyek Pemrograman untuk {self._nama_siswa}")
        while True:
            try:
                jumlah_tes = int(input("Masukkan jumlah total test case: "))
                tes_lulus = int(input("Masukkan jumlah test case yang lulus: "))
                if tes_lulus > jumlah_tes:
                     raise ValueError("Tes lulus tidak boleh lebih besar dari jumlah tes.")
                break
            except ValueError as e:
                print(f"Input tidak valid: {e}. Silakan coba lagi.")
        
        if self._jumlah_tes == 0:
            nilai_akhir = 0
        else:
            nilai_akhir = (tes_lulus / jumlah_tes) * 100
        
        self.set_nilai(nilai_akhir)
        print(f"Hasil: {tes_lulus} dari {jumlah_tes} tes lulus. Nilai Akhir: {self.get_nilai():.2f}")


class PresentasiLisan(DokumenAkademik):
    def __init__(self, nama_siswa, id_siswa):
        super().__init__(nama_siswa, id_siswa)

    def proses_penilaian(self):
        print(f"\nMenilai Presentasi Lisan untuk {self._nama_siswa}")
        while True:
            try:
                nilai_kelancaran = float(input("Masukkan nilai kelancaran (0-100): "))
                nilai_materi = float(input("Masukkan nilai penguasaan materi (0-100): "))
                if not (0 <= nilai_kelancaran <= 100 and 0 <= nilai_materi <= 100):
                    raise ValueError("Nilai harus di antara 0 dan 100.")
                break
            except ValueError as e:
                print(f"Input tidak valid: {e}. Silakan coba lagi.")
        
        nilai_akhir = (nilai_kelancaran + nilai_materi) / 2
        self.set_nilai(nilai_akhir)
        print(f"Nilai Presentasi Akhir: {self.get_nilai():.2f}")


def dapatkan_kunci_jawaban():
    while True:
        try:
            jumlah_soal = int(input("Masukkan total jumlah soal pilihan ganda: "))
            if jumlah_soal <= 0:
                print("Jumlah soal harus lebih dari 0.")
                continue
            
            kunci = input(f"Masukkan {jumlah_soal} kunci jawaban (contoh: ABCDA): ").upper().strip()
            
            if len(kunci) != jumlah_soal:
                print(f"Error: Anda memasukkan {len(kunci)} jawaban, seharusnya {jumlah_soal}.")
                continue
            
            return kunci
        except ValueError:
            print("Input tidak valid. Harap masukkan angka untuk jumlah soal.")


if __name__ == "__main__":
    daftar_nilai_siswa = {}

    
    print("      PENGATURAN KUNCI JAWABAN            ")
    
    kunci_jawaban_pg = dapatkan_kunci_jawaban()
    
    while True:
        
        print("      MASUKKAN DATA SISWA BARU            ")
        
        nama = input("Masukkan nama siswa: ")
        id_siswa = input("Masukkan ID siswa: ")

        print("\nPilih Jenis Dokumen untuk Dinilai:")
        print("1. Ujian Pilihan Ganda")
        print("2. Tugas Esai")
        print("3. Proyek Pemrograman")
        print("4. Presentasi Lisan")
        pilihan = input("Masukkan pilihan (1-4): ")

        dokumen = None
        if pilihan == '1':
            dokumen = UjianPilihanGanda(nama, id_siswa, kunci_jawaban_pg)
        elif pilihan == '2':
            dokumen = TugasEsai(nama, id_siswa)
        elif pilihan == '3':
            dokumen = ProyekPemrograman(nama, id_siswa)
        elif pilihan == '4':
            dokumen = PresentasiLisan(nama, id_siswa)
        else:
            print("Pilihan tidak valid.")
            continue
        
        dokumen.proses_penilaian()
        daftar_nilai_siswa[nama] = {
            "ID": id_siswa,
            "Nilai": dokumen.get_nilai()
        }

        lanjut = input("\nApakah Anda ingin menambah siswa lain? (y/t): ").lower()
        if lanjut != 'y':
            break

    print("        LAPORAN NILAI AKHIR             ")
    
    if not daftar_nilai_siswa:
        print("Tidak ada data siswa yang diproses.")
    else:
        for nama, data in daftar_nilai_siswa.items():
            print(f"Nama: {nama}, ID: {data['ID']}, Nilai: {data['Nilai']:.2f}")

