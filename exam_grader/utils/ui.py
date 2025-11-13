import os

class UserInterface:
    def display_main_menu(self) -> str:
        print("\n" + "="*50)
        print("         WELCOME TO EZ EXAM GRADER!")
        print("📚 Malas Cek Nilai Sendiri? We Gotchu! 🖊️")
        print("="*50)
        print("Menu:")
        print("  1. Cara Pemakaian")
        print("  2. Mulai Penilaian")
        print("  3. Keluar")
        
        choice = input("Pilih menu (1-3): ")
        return choice

    def display_how_to_use(self):
        print("\n--- Cara Pemakaian EZ Exam Grader ---")
        print("1. Siapkan Kunci Jawaban: Program akan meminta path ke file .json kunci jawaban.")
        print("2. Siapkan Jawaban Siswa: Program akan meminta path ke folder yang berisi file .json jawaban siswa.")
        print("3. Penilaian Otomatis: Program akan menilai soal Pilihan Ganda dan Jawaban Singkat secara otomatis.")
        print("4. Penilaian Manual: Untuk soal Esai, program akan menampilkan jawaban siswa dan meminta Anda memasukkan nilai.")
        print("5. Laporan Excel: Setelah selesai, program akan membuat laporan nilai dalam format Excel di folder 'output'.")
        input("\nTekan Enter untuk kembali ke menu utama...")

    def get_grading_paths(self) -> tuple[str, str]:
        print("\n--- Memulai Sesi Penilaian ---")
        
        student_answers_path = ""
        while not os.path.isdir(student_answers_path):
            student_answers_path = input("Masukkan path ke folder jawaban siswa: ")
            if not os.path.isdir(student_answers_path):
                print(f"Error: Direktori tidak ditemukan di '{student_answers_path}'. Silakan coba lagi.")

        answer_key_path = ""
        while not os.path.isfile(answer_key_path):
            answer_key_path = input("Masukkan path ke file kunci jawaban (.json): ")
            if not os.path.isfile(answer_key_path):
                print(f"Error: File tidak ditemukan di '{answer_key_path}'. Silakan coba lagi.")
        
        print("\nPath diterima. Memulai proses penilaian...\n")
        return student_answers_path, answer_key_path

    def prompt_for_essay_score(self, student_name: str, student_answer: str, question_prompt: str, max_points: int) -> float:
        print("\n" + "-"*25 + f" Penilaian Manual untuk: {student_name} " + "-"*25)
        print(f"Pertanyaan:  {question_prompt}")
        print(f"Jawaban Siswa: \"{student_answer}\"")
        
        score = -1.0
        while score < 0 or score > max_points:
            try:
                score_input = input(f"Masukkan nilai (0-{max_points}): ")
                score = float(score_input)
                if score < 0 or score > max_points:
                    print(f"Error: Nilai harus di antara 0 dan {max_points}.")
            except ValueError:
                print("Error: Harap masukkan angka yang valid.")
        
        return score

    def display_progress(self, message: str):
        print(message)
    
    def display_exit_message(self):
        print("\nTerima kasih telah menggunakan EZ Exam Grader! Sampai jumpa!")