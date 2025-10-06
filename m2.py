class Grader:
  def run(self):
    print("Mulai Mengecek!")
    print("\n1. Ya")
    print("2. Tidak")

    choice = input("\nMulai sekarang? (1/2): ")

    if choice == "1":
      self.process_grading()
    elif choice == "2":
      print("\nSemoga harimu menyenangkan!")
    else:
      print("\nGoodbye.")
      self.run()


class ManualGrader(Grader):
  def process_grading(self):
    while True:
      print("\n--- Mulai Pemeriksaan Manual ---")

      nama_siswa = input("\nMasukkan nama siswa: ")
      while True:
        no_siswa = input("Nomor Induk Siswa: ")
        if no_siswa.isdigit():
          break
        else:
          print("Input tidak valid. Harap masukkan angka saja untuk ID.")
      mata_pelajaran = input("Mata Pelajaran: ")
      kelas = input("Kelas: ")

      try:
        jumlah_soal = int(input("Jumlah soal: "))
        if jumlah_soal == 0:
            print("\nError: Jumlah soal tidak boleh nol.")
            lanjut = input("\nCek lembar lain? (y/t): ")
            if lanjut.lower() != "y":
                break
            else:
                continue

        jawaban_benar = int(input("Jumlah jawaban benar: "))

        if jumlah_soal < jawaban_benar:
          print("\nError: Jumlah jawaban benar tidak boleh lebih besar dari jumlah soal.")
          continue

        nilai_per_soal = 100 / jumlah_soal
        nilai_akhir = jawaban_benar * nilai_per_soal

        print("\nLaporan Nilai")
        print(f"Nama           : {nama_siswa}")
        print(f"NIS            : {no_siswa}")
        print(f"Mata Pelajaran : {mata_pelajaran}")
        print(f"Kelas          : {kelas}")
        print(f"Nilai          : {nilai_akhir:.2f}")

      except ValueError:
        print("\nInput tidak valid. Harap masukkan angka yang valid untuk jumlah soal dan jawaban benar.")
      
      lanjut = input("\nApakah Anda ingin memeriksa lembar lain? (y/t): ")
      if lanjut.lower() != "y":
        break

    print("\nTerima Kasih telah menggunakan sistem penilaian kami!")


if __name__ == "__main__":
  grader = ManualGrader()
  grader.run()

