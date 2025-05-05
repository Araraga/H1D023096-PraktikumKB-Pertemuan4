import tkinter as tk
from tkinter import ttk
from pyswip import Prolog

prolog = Prolog()
prolog.consult("jaringan_diagnosa.pl")

pertanyaan_fakta = [
    ("Apakah Anda tidak bisa mengakses internet?", "tidak_ada_akses"),
    ("Apakah perangkat Anda terhubung ke Wi-Fi?", "terhubung_wifi"),
    ("Apakah hanya perangkat Anda yang bermasalah?", "hanya_perangkat_ini"),
    ("Apakah semua perangkat mengalami masalah?", "semua_terpengaruh"),
    ("Apakah terdapat ikon tanda seru di status jaringan?", "ada_tanda_seru"),
    ("Apakah DNS tidak merespons saat browsing?", "dns_tidak_merespon"),
    ("Apakah ping Anda tinggi saat uji koneksi?", "ping_tinggi"),
    ("Apakah Anda menggunakan kabel LAN (ethernet)?", "menggunakan_ethernet"),
    ("Apakah perangkat tidak terhubung ke Wi-Fi?", "tidak_terhubung_wifi")
]

index_pertanyaan = 0

def tampilkan_pertanyaan():
    if index_pertanyaan < len(pertanyaan_fakta):
        kotak_pertanyaan.config(state="normal")
        kotak_pertanyaan.delete("1.0", tk.END)
        kotak_pertanyaan.insert(tk.END, pertanyaan_fakta[index_pertanyaan][0])
        kotak_pertanyaan.config(state="disabled")
    else:
        lakukan_diagnosa()

def proses_jawaban(ya):
    global index_pertanyaan
    fakta = pertanyaan_fakta[index_pertanyaan][1]
    if ya:
        prolog.assertz(f"fakta({fakta})")
    index_pertanyaan += 1
    tampilkan_pertanyaan()

def lakukan_diagnosa():
    hasil = list(prolog.query("diagnosa(Diagnosis)"))
    if hasil:
        diagnosis = hasil[0]["Diagnosis"]
        solusi = list(prolog.query(f"solusi('{diagnosis}', Solusi)"))[0]["Solusi"]
        hasil_var.set(f"🩺 Diagnosis:\n{diagnosis}\n\n💡 Solusi:\n{solusi}")
    else:
        hasil_var.set("❌ Diagnosis tidak ditemukan. Coba ulangi dan periksa jawaban Anda.")

    yes_btn.config(state=tk.DISABLED)
    no_btn.config(state=tk.DISABLED)
    ulang_btn.config(state=tk.NORMAL)

def reset_diagnosis():
    global index_pertanyaan
    index_pertanyaan = 0
    prolog.retractall("fakta(_)")
    hasil_var.set("")
    yes_btn.config(state=tk.NORMAL)
    no_btn.config(state=tk.NORMAL)
    ulang_btn.config(state=tk.DISABLED)
    tampilkan_pertanyaan()

root = tk.Tk()
root.title("Sistem Pakar Jaringan Komputer")
root.geometry("620x460")
root.configure(bg="#eef2f5")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Sistem Pakar Diagnosa Masalah Jaringan", style="Title.TLabel").pack(pady=(0, 10))
ttk.Label(frame, text="Jawab pertanyaan berikut:").pack(anchor="w")

ttk.Label(frame, text="Pertanyaan:", font=("Segoe UI", 10, "bold")).pack(anchor="w")

kotak_pertanyaan = tk.Text(frame, height=3, width=70, wrap="word", font=("Segoe UI", 11), relief="solid")
kotak_pertanyaan.pack(pady=5)
kotak_pertanyaan.config(state="disabled")

btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=10)

yes_btn = ttk.Button(btn_frame, text="Ya", command=lambda: proses_jawaban(True))
yes_btn.grid(row=0, column=0, padx=10)

no_btn = ttk.Button(btn_frame, text="Tidak", command=lambda: proses_jawaban(False))
no_btn.grid(row=0, column=1, padx=10)

ulang_btn = ttk.Button(btn_frame, text="🔁 Diagnosis Ulang", command=reset_diagnosis, state=tk.DISABLED)
ulang_btn.grid(row=0, column=2, padx=10)

hasil_var = tk.StringVar()
hasil_label = ttk.Label(frame, textvariable=hasil_var, wraplength=550, justify="left", foreground="blue")
hasil_label.pack(pady=20)

tampilkan_pertanyaan()
root.mainloop()
