def main_menu():
  print("Start Grading your student's exam paper here!")
  print("\n1. Yes")
  print("2. No")

  choice = input("\nStart now? (1/2): ")

  if choice == "1":
    start_grading()
  elif choice == "2":
    print("\nHave a good day!")
  else:
    print("\nInvalid choice. Please try again.")
    main_menu()

def start_grading():
  print("\nStart grading now!")

  nama_siswa = input("\nEnter student's name: ")
  while True:
    no_siswa = input("Student's ID: ")
    if no_siswa.isdigit():
      break
    else:
      print("Input Number")
  mata_pelajaran = input("Subject: ")
  kelas = input("Class: ")

  try:
    jumlah_soal = int(input("Number of questions: "))
    jawaban_benar = int(input("Number of correct answers: "))

    if jumlah_soal < jawaban_benar:
      print("\nInvalid input. Number of correct answers cannot be greater than the number of questions.")
      return

    nilai_per_soal = 100 / jumlah_soal
    nilai_akhir = jawaban_benar * nilai_per_soal

    print(f"\nName    : {nama_siswa}")
    print(f"ID      : {no_siswa}")
    print(f"Subject : {mata_pelajaran}")
    print(f"Class   : {kelas}")
    print(f"Score   : {nilai_akhir:.2f}")

    lanjut = input("\nDo you want to continue? (y/n): ")
    if lanjut.lower() == "y":
      start_grading()
    else:
      print("\nThank You for using our grading system!")

  except ValueError:
    print("\nInvalid input. Please enter a valid number for the number of questions and correct answers.")
    return


main_menu()