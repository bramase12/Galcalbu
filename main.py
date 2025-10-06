import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

# Ini adalah Class utama aplikasi kita, anggap saja sebagai "Manajer Panggung"
class AplikasiBisnis(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Konfigurasi jendela utama
        self.title("Kalkulator Cuan Bisnis")
        self.geometry("500x550")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        # Ini adalah "wadah" utama tempat semua scene (frame) akan ditumpuk
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary untuk menyimpan semua scene kita
        self.frames = {}
        # List untuk menyimpan data bahan baku
        self.bahan_list = []

        # Membuat dan menyimpan setiap scene
        for F in (MainMenu, TabelBahan, TotalUntungRugi):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Menampilkan scene pertama yaitu MainMenu
        self.show_frame("MainMenu")

    # Fungsi untuk pindah scene
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        # Jika scene yang dituju adalah TotalUntungRugi, kita update dulu datanya
        if page_name == "TotalUntungRugi":
            frame.update_display()
        frame.tkraise()

# SCENE 1: Main Menu (Halaman Utama)
class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Kalkulator Cuan Bisnis", font=controller.title_font, pady=20)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Input Bahan Produksi",
                            command=lambda: controller.show_frame("TabelBahan"),
                            height=3, width=30)
        button2 = tk.Button(self, text="Hitung Untung/Rugi",
                            command=lambda: controller.show_frame("TotalUntungRugi"),
                            height=3, width=30)
        button1.pack(pady=10)
        button2.pack(pady=10)

# SCENE 2: Tabel Bahan-Bahan Produksi
class TabelBahan(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Input Bahan Produksi", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # Frame untuk input form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nama Bahan:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nama_bahan_entry = tk.Entry(form_frame, width=30)
        self.nama_bahan_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Harga Satuan (Rp):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.harga_bahan_entry = tk.Entry(form_frame, width=30)
        self.harga_bahan_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Jumlah:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.jumlah_bahan_entry = tk.Entry(form_frame, width=30)
        self.jumlah_bahan_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Tombol Tambah
        add_button = tk.Button(form_frame, text="Tambah Bahan", command=self.tambah_bahan)
        add_button.grid(row=3, columnspan=2, pady=10)

        # Listbox untuk menampilkan daftar bahan
        self.bahan_listbox = tk.Listbox(self, height=10, width=60)
        self.bahan_listbox.pack(pady=10)

        # Tombol kembali
        back_button = tk.Button(self, text="Kembali ke Menu",
                                command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def tambah_bahan(self):
        nama = self.nama_bahan_entry.get()
        harga_str = self.harga_bahan_entry.get()
        jumlah_str = self.jumlah_bahan_entry.get()

        # Validasi: pastikan semua kolom diisi
        if not nama or not harga_str or not jumlah_str:
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return

        try:
            # Konversi harga dan jumlah ke angka
            harga = float(harga_str)
            jumlah = int(jumlah_str)
        except ValueError:
            messagebox.showerror("Error", "Harga dan Jumlah harus berupa angka!")
            return

        # Simpan data bahan ke list di controller
        bahan_data = {"nama": nama, "harga": harga, "jumlah": jumlah}
        self.controller.bahan_list.append(bahan_data)

        # Update tampilan di Listbox
        self.update_listbox()
        
        # Kosongkan kolom isian setelah ditambahkan
        self.nama_bahan_entry.delete(0, tk.END)
        self.harga_bahan_entry.delete(0, tk.END)
        self.jumlah_bahan_entry.delete(0, tk.END)
        
    def update_listbox(self):
        # Hapus semua item lama
        self.bahan_listbox.delete(0, tk.END)
        # Tambahkan semua item baru dari data
        for item in self.controller.bahan_list:
            total_harga_item = item['harga'] * item['jumlah']
            display_text = f"{item['nama']} ({item['jumlah']} pcs) - Rp {total_harga_item:,.2f}"
            self.bahan_listbox.insert(tk.END, display_text)

# SCENE 3: Total Untung/Rugi
class TotalUntungRugi(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Perhitungan Untung/Rugi", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # Frame untuk input penjualan
        penjualan_frame = tk.Frame(self)
        penjualan_frame.pack(pady=10)

        tk.Label(penjualan_frame, text="Harga Jual Produk (Rp):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.harga_jual_entry = tk.Entry(penjualan_frame, width=25)
        self.harga_jual_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(penjualan_frame, text="Jumlah Produk Terjual:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.jumlah_terjual_entry = tk.Entry(penjualan_frame, width=25)
        self.jumlah_terjual_entry.grid(row=1, column=1, padx=5, pady=5)

        hitung_button = tk.Button(penjualan_frame, text="HITUNG", command=self.hitung_untung_rugi)
        hitung_button.grid(row=2, columnspan=2, pady=10)

        # Frame untuk menampilkan hasil
        hasil_frame = tk.Frame(self, bd=2, relief="groove")
        hasil_frame.pack(pady=20, padx=20, fill="x")

        tk.Label(hasil_frame, text="--- HASIL PERHITUNGAN ---", font=("Helvetica", 12, "bold")).pack(pady=5)
        
        self.total_modal_label = tk.Label(hasil_frame, text="Total Modal: Rp 0", font=("Helvetica", 10))
        self.total_modal_label.pack(anchor="w", padx=10)

        self.total_pemasukan_label = tk.Label(hasil_frame, text="Total Pemasukan: Rp 0", font=("Helvetica", 10))
        self.total_pemasukan_label.pack(anchor="w", padx=10)

        self.hasil_label = tk.Label(hasil_frame, text="Status: -", font=("Helvetica", 14, "bold"))
        self.hasil_label.pack(pady=10)

        back_button = tk.Button(self, text="Kembali ke Menu",
                                command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=10)

    def update_display(self):
        # Fungsi ini akan menghitung total modal dari data bahan dan menampilkannya
        total_modal = sum(item['harga'] * item['jumlah'] for item in self.controller.bahan_list)
        self.total_modal_label.config(text=f"Total Modal: Rp {total_modal:,.2f}")
        # Reset hasil perhitungan lainnya saat kembali ke halaman ini
        self.total_pemasukan_label.config(text="Total Pemasukan: Rp 0")
        self.hasil_label.config(text="Status: -", fg="black")


    def hitung_untung_rugi(self):
        harga_jual_str = self.harga_jual_entry.get()
        jumlah_terjual_str = self.jumlah_terjual_entry.get()
        
        if not harga_jual_str or not jumlah_terjual_str:
            messagebox.showerror("Error", "Harga Jual dan Jumlah Terjual harus diisi!")
            return

        try:
            harga_jual = float(harga_jual_str)
            jumlah_terjual = int(jumlah_terjual_str)
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa angka!")
            return

        # Hitung total modal dari list bahan
        total_modal = sum(item['harga'] * item['jumlah'] for item in self.controller.bahan_list)
        # Hitung total pemasukan
        total_pemasukan = harga_jual * jumlah_terjual
        
        # Hitung untung/rugi
        hasil = total_pemasukan - total_modal

        # Update label hasil
        self.total_modal_label.config(text=f"Total Modal: Rp {total_modal:,.2f}")
        self.total_pemasukan_label.config(text=f"Total Pemasukan: Rp {total_pemasukan:,.2f}")

        if hasil > 0:
            self.hasil_label.config(text=f"UNTUNG: Rp {hasil:,.2f}", fg="green")
        elif hasil < 0:
            self.hasil_label.config(text=f"RUGI: Rp {abs(hasil):,.2f}", fg="red")
        else:
            self.hasil_label.config(text="IMPAS (BEP)", fg="blue")

# Ini adalah bagian yang akan menjalankan aplikasi kita
if __name__ == "__main__":
    app = AplikasiBisnis()
    app.mainloop()