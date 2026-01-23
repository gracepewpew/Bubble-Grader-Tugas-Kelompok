import os
# Import interface kontrak tadi
from ..grading.grading_types import IScoreInputProvider

# UI kita implementasi IScoreInputProvider.
# Artinya: "Oke, saya berjanji bisa nyediain input nilai buat EssayGrader."
class UserInterface(IScoreInputProvider):
    
    #  SRP (Single Responsibility Principle) 
    # Tugas class ini CUMA ngurusin print ke layar dan terima input user.
    # Dia gak boleh nge-load file JSON (tugas FileManager) atau ngitung nilai (tugas Grader).
    
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
        print("\n Cara Pemakaian EZ Exam Grader ")
        print("1. Program akan membaca mapel otomatis dari folder 'input_data'.")
        print("2. Pilih Mapel dan Kelas dari menu yang tersedia.")
        print("3. Penilaian Otomatis berjalan.")
        input("\nTekan Enter untuk kembali ke menu utama...")

    def get_grading_paths(self, file_manager) -> tuple[str, str]:
        print("\n Memilih Mapel & Kelas ")
        
        subjects = file_manager.get_available_subjects()
        if not subjects:
            print("❌ Error: Tidak ada folder mata pelajaran ditemukan di input_data/answer_keys/.")
            return "", ""
            
        print("Mata Pelajaran yang tersedia:")
        for idx, sub in enumerate(subjects):
            print(f"  {idx + 1}. {sub}")
            
        try:
            sub_idx = int(input("Pilih nomor mapel: ")) - 1
            if sub_idx < 0 or sub_idx >= len(subjects): 
                raise ValueError
            selected_subject = subjects[sub_idx]
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")
            return "", ""
        
        keys = file_manager.get_keys_for_subject(selected_subject)
        if not keys:
            print(f"❌ Error: Tidak ada file kunci jawaban di folder {selected_subject}.")
            return "", ""
            
        print(f"\nKelas/Kunci untuk {selected_subject}:")
        for idx, key in enumerate(keys):
            print(f"  {idx + 1}. {key}")
            
        try:
            key_idx = int(input("Pilih nomor kunci jawaban: ")) - 1
            if key_idx < 0 or key_idx >= len(keys):
                raise ValueError
            selected_key_filename = keys[key_idx]
        except (ValueError, IndexError):
             print("Pilihan tidak valid.")
             return "", ""
        
        answer_key_path = file_manager.get_full_key_path(selected_subject, selected_key_filename)
        student_answers_path = os.path.join("input_data", "student_answers", selected_subject)
        
        print(f"\n✅ Menggunakan Kunci: {selected_key_filename}")
        print(f"✅ Mencari jawaban siswa di: {student_answers_path}\n")
        
        return student_answers_path, answer_key_path

    # Ini method 'Wajib' karena kita implementasi IScoreInputProvider
    def get_essay_score(self, student_name: str, student_answer: str, question_prompt: str, max_points: int) -> float:
        print("\n" + "-"*25 + f" Penilaian Manual untuk: {student_name} " + "-"*25)
        print(f"Pertanyaan:  {question_prompt}")
        print(f"Jawaban Siswa: \"{student_answer}\"")
        score = -1.0
        while score < 0 or score > max_points:
            try:
                score = float(input(f"Masukkan nilai (0-{max_points}): "))
            except ValueError:
                pass
        return score

    def display_progress(self, message: str):
        print(message)
    
    def display_exit_message(self):
        print("\nBye bye!")