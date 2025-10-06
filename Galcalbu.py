import tkinter as tk
from tkinter import ttk, font as tkfont, messagebox
import json
# Import ttkbootstrap
import ttkbootstrap as ttkb 
from ttkbootstrap.constants import * # Mengimpor konstanta ttkbootstrap

# ==============================================================================
# KELAS UTAMA APLIKASI (CONTROLLER)
# Menggunakan ttkbootstrap.Window
# ==============================================================================
class AplikasiBisnis(ttkb.Window): # <--- PERUBAHAN UTAMA: Mengganti tk.Tk menjadi ttkb.Window
    def __init__(self, *args, **kwargs):
        # Kita bisa memilih tema di sini. Contoh: 'superhero' untuk gelap
        # Pilihan bagus lainnya: 'darkly', 'litera' (terang), 'flatly' (terang)
        super().__init__(themename="superhero", *args, **kwargs) # <--- TEMA GELAP DEFAULT!

        # Konfigurasi jendela utama
        self.title("GALCALBU - Business Calculator")
        self.geometry("800x650") # Sedikit lebih besar
        self.title_font = tkfont.Font(family='Helvetica', size=22, weight="bold")
        self.theme_name = "superhero" # Menyimpan nama tema saat ini

        # Wadah utama untuk semua scene
        container = ttkb.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Penyimpanan data
        self.bahan_pokok = []
        self.bahan_penunjang = []
        self.load_data() 

        # Dictionary untuk menyimpan semua scene
        self.frames = {}
        for F in (MainMenu, SceneInputBarang, SceneHitungLaba):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """Fungsi untuk berpindah halaman/scene."""
        frame = self.frames[page_name]
        # Update tampilan jika menuju halaman tertentu
        if page_name == "SceneHitungLaba":
            frame.update_display()
        frame.tkraise()

    def save_data(self):
        """Menyimpan data ke file JSON."""
        data_to_save = {
            "bahan_pokok": self.bahan_pokok,
            "bahan_penunjang": self.bahan_penunjang
        }
        try:
            with open("data_bisnis.json", "w") as f:
                json.dump(data_to_save, f, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

    def load_data(self):
        """Memuat data dari file JSON."""
        try:
            with open("data_bisnis.json", "r") as f:
                data = json.load(f)
                self.bahan_pokok = data.get("bahan_pokok", [])
                self.bahan_penunjang = data.get("bahan_penunjang", [])
        except FileNotFoundError:
            pass 
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")
            
    # <-- FUNGSI BARU: Mengubah Tema Aplikasi
    def toggle_theme(self):
        """Mengganti tema antara terang (litera) dan gelap (superhero)."""
        if self.theme_name == "superhero":
            new_theme = "litera"
            self.theme_name = "litera"
        else:
            new_theme = "superhero"
            self.theme_name = "superhero"
            
        # Mengubah tema secara dinamis
        self.style.theme_use(new_theme)
        # Warna teks label utama diubah agar tetap kontras
        for frame in self.frames.values():
            if hasattr(frame, 'main_label'):
                frame.main_label.config(foreground="white" if self.theme_name == "superhero" else "black")


# ==============================================================================
# SCENE 1: MAIN MENU
# ==============================================================================
class MainMenu(ttkb.Frame): # Mengganti tk.Frame menjadi ttkb.Frame
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller
        
        # Label utama
        self.main_label = ttkb.Label(self, text="GALCALBU Business Calculator", font=controller.title_font)
        self.main_label.pack(side="top", fill="x", pady=(20, 40))
        
        # Tombol Navigasi
        # Menggunakan 'primary' dan style 'outline' untuk kesan modern
        button1 = ttkb.Button(self, text="▶️ Input Data Bahan", command=lambda: controller.show_frame("SceneInputBarang"), bootstyle="primary", width=30)
        button2 = ttkb.Button(self, text="📊 Hitung Laba & Rugi", command=lambda: controller.show_frame("SceneHitungLaba"), bootstyle="success", width=30)
        
        # Tombol Tema Baru
        theme_button = ttkb.Button(self, text="Toggle Tema Terang/Gelap 🌗", command=controller.toggle_theme, bootstyle="warning", width=30)
        
        button1.pack(pady=15, ipady=10)
        button2.pack(pady=15, ipady=10)
        theme_button.pack(pady=30, ipady=5)


# ==============================================================================
# SCENE 2: INPUT DATA BAHAN
# ==============================================================================
class SceneInputBarang(ttkb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.main_label = ttkb.Label(self, text="Input Data Bahan", font=controller.title_font)
        self.main_label.pack(side="top", fill="x", pady=10)

        notebook = ttkb.Notebook(self)
        notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Membuat frame untuk setiap tab
        self.frame_pokok = ttkb.Frame(notebook, padding=10)
        self.frame_penunjang = ttkb.Frame(notebook, padding=10)
        notebook.add(self.frame_pokok, text="Bahan Pokok")
        notebook.add(self.frame_penunjang, text="Bahan Penunjang")

        # Setup isi untuk setiap tab
        self.setup_tab(self.frame_pokok, "Bahan Pokok", self.controller.bahan_pokok, self.add_item_pokok)
        self.setup_tab(self.frame_penunjang, "Bahan Penunjang", self.controller.bahan_penunjang, self.add_item_penunjang)

        back_button = ttkb.Button(self, text="⬅️ Kembali ke Menu", command=lambda: controller.show_frame("MainMenu"), bootstyle="secondary-outline")
        back_button.pack(pady=10)

    def setup_tab(self, parent_frame, title, data_list, add_command):
        form = ttkb.Frame(parent_frame, padding=10, relief=tk.RAISED) # Menambahkan relief
        form.pack(pady=10, padx=10, fill="x")

        # Layout input menggunakan Grid untuk kontrol yang lebih baik
        ttkb.Label(form, text="Nama:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttkb.Entry(form, width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttkb.Label(form, text="Harga:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        price_entry = ttkb.Entry(form, width=15)
        price_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttkb.Label(form, text="Jumlah:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        qty_entry = ttkb.Entry(form, width=10)
        qty_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # Membuat kolom terakhir (tombol) lebih kecil
        form.grid_columnconfigure(1, weight=3) # Nama
        form.grid_columnconfigure(3, weight=2) # Harga
        form.grid_columnconfigure(5, weight=1) # Jumlah
        
        # Frame untuk tombol-tombol
        button_frame = ttkb.Frame(form)
        button_frame.grid(row=0, column=6, padx=10, sticky="e")

        # Tombol Tambah menggunakan style 'success'
        add_btn = ttkb.Button(button_frame, text="➕ Tambah", command=lambda: add_command(name_entry, price_entry, qty_entry, tree), bootstyle="success")
        add_btn.pack(side=tk.LEFT, padx=5)

        # Tombol Hapus menggunakan style 'danger'
        delete_btn = ttkb.Button(button_frame, text="🗑️ Hapus", command=lambda: self.delete_item(tree, data_list), bootstyle="danger")
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Area Treeview untuk menampilkan data
        # Menggunakan style 'primary' untuk Treeview
        tree = ttkb.Treeview(parent_frame, columns=("Nama", "Harga", "Jumlah", "Total"), show="headings", bootstyle="primary")
        tree.heading("Nama", text="Nama Barang")
        tree.heading("Harga", text="Harga Satuan")
        tree.heading("Jumlah", text="Jumlah")
        tree.heading("Total", text="Total Harga")
        # Mengatur lebar kolom agar lebih proporsional
        tree.column("Nama", width=150, anchor=tk.W)
        tree.column("Harga", width=100, anchor=tk.E)
        tree.column("Jumlah", width=80, anchor=tk.CENTER)
        tree.column("Total", width=120, anchor=tk.E)
        
        # Scrollbar untuk Treeview
        vsb = ttkb.Scrollbar(parent_frame, orient="vertical", command=tree.yview, bootstyle="round")
        tree.configure(yscrollcommand=vsb.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        vsb.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))

        self.populate_tree(tree, data_list)

        return name_entry, price_entry, qty_entry, tree
    
    # Fungsi delete_item, add_item_pokok, add_item_penunjang, add_item_to_list, populate_tree
    # Semua fungsi ini tidak perlu diubah secara fungsional, hanya perlu memastikan 
    # widget messagebox berasal dari tkinter (bukan ttkb) agar tetap standar.
    
    def delete_item(self, tree, data_list):
        """Fungsi untuk menghapus item yang dipilih dari Treeview dan data list."""
        selected_items = tree.selection() 
        if not selected_items:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin Anda hapus terlebih dahulu.")
            return

        selected_item = selected_items[0]

        if messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data ini secara permanen?"):
            try:
                item_index = tree.index(selected_item)
                data_list.pop(item_index)
                tree.delete(selected_item)
                self.controller.save_data()
                messagebox.showinfo("Sukses", "Data berhasil dihapus.")
            except IndexError:
                messagebox.showerror("Error", "Terjadi kesalahan saat mencoba menghapus data.")

    def add_item_pokok(self, name_entry, price_entry, qty_entry, tree):
        self.add_item_to_list(name_entry, price_entry, qty_entry, tree, self.controller.bahan_pokok)

    def add_item_penunjang(self, name_entry, price_entry, qty_entry, tree):
        self.add_item_to_list(name_entry, price_entry, qty_entry, tree, self.controller.bahan_penunjang)

    def add_item_to_list(self, name_entry, price_entry, qty_entry, tree, data_list):
        """Logika untuk menambah item baru."""
        name = name_entry.get()
        try:
            price = float(price_entry.get())
            qty = int(qty_entry.get())
            if not name:
                messagebox.showerror("Error", "Nama barang tidak boleh kosong!")
                return
            
            total = price * qty
            item_data = {"name": name, "price": price, "quantity": qty, "total": total}
            data_list.append(item_data)
            
            # Update Treeview
            tree.insert("", "end", values=(name, f"Rp {price:,.2f}", qty, f"Rp {total:,.2f}"))
            
            # Kosongkan form
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)

            self.controller.save_data() # Simpan data setiap kali ada penambahan

        except ValueError:
            messagebox.showerror("Error", "Harga dan Jumlah harus berupa angka!")

    def populate_tree(self, tree, data_list):
        """Mengisi tabel dengan data yang sudah ada saat aplikasi dibuka."""
        for item in data_list:
            tree.insert("", "end", values=(
                item["name"], 
                f"Rp {item['price']:,.2f}", 
                item["quantity"], 
                f"Rp {item['total']:,.2f}"
            ))


# ==============================================================================
# SCENE 3: HITUNG LABA & RUGI
# ==============================================================================
class SceneHitungLaba(ttkb.Frame): # Mengganti tk.Frame menjadi ttkb.Frame
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.main_label = ttkb.Label(self, text="Perhitungan Laba & Rugi", font=controller.title_font)
        self.main_label.pack(side="top", fill="x", pady=20)

        # Frame untuk input penjualan
        penjualan_frame = ttkb.Frame(self, padding=10, relief=tk.GROOVE)
        penjualan_frame.pack(pady=10, padx=20, fill="x")
        
        # Menggunakan Label dan Entry dari ttkbootstrap
        ttkb.Label(penjualan_frame, text="Harga Jual Satuan (Rp):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.harga_jual_entry = ttkb.Entry(penjualan_frame, width=25)
        self.harga_jual_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttkb.Label(penjualan_frame, text="Jumlah Produk Terjual:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.jumlah_terjual_entry = ttkb.Entry(penjualan_frame, width=25)
        self.jumlah_terjual_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Tombol Hitung yang lebih mencolok
        hitung_button = ttkb.Button(penjualan_frame, text="HITUNG LABA 🚀", command=self.hitung_laba_rugi, bootstyle="primary")
        hitung_button.grid(row=2, columnspan=2, pady=15)

        # Frame untuk menampilkan hasil - menggunakan style 'info'
        hasil_frame = ttkb.Frame(self, padding=15, bootstyle="secondary")
        hasil_frame.pack(pady=20, padx=20, fill="x")
        
        ttkb.Label(hasil_frame, text="--- HASIL PERHITUNGAN ---", font=("Helvetica", 14, "bold")).pack(pady=5)
        
        # Rincian Modal
        self.modal_pokok_label = ttkb.Label(hasil_frame, text="Modal Pokok: Rp 0", font=("Helvetica", 11))
        self.modal_pokok_label.pack(anchor="w", padx=10, pady=3)
        self.modal_penunjang_label = ttkb.Label(hasil_frame, text="Modal Penunjang: Rp 0", font=("Helvetica", 11))
        self.modal_penunjang_label.pack(anchor="w", padx=10, pady=3)
        self.total_modal_label = ttkb.Label(hasil_frame, text="Total Modal Keseluruhan: Rp 0", font=("Helvetica", 12, "bold"))
        self.total_modal_label.pack(anchor="w", padx=10, pady=(10,5))

        # Pemasukan dan Hasil Akhir
        self.total_pemasukan_label = ttkb.Label(hasil_frame, text="Total Pemasukan: Rp 0", font=("Helvetica", 12, "bold"))
        self.total_pemasukan_label.pack(anchor="w", padx=10, pady=(10,5))
        
        # Separator (garis pemisah) untuk tampilan yang lebih rapi
        ttkb.Separator(hasil_frame, orient=HORIZONTAL).pack(fill="x", pady=10)
        
        self.margin_label = ttkb.Label(hasil_frame, text="Margin: 0.00%", font=("Helvetica", 14, "bold"), bootstyle="warning") # Warna oranye/kuning
        self.margin_label.pack(pady=(10,5))
        self.hasil_label = ttkb.Label(hasil_frame, text="Status: -", font=("Helvetica", 20, "bold"))
        self.hasil_label.pack(pady=(5,15))

        back_button = ttkb.Button(self, text="⬅️ Kembali ke Menu", command=lambda: controller.show_frame("MainMenu"), bootstyle="secondary-outline")
        back_button.pack(pady=10)

    def update_display(self):
        """Update tampilan modal saat halaman ini dibuka."""
        # Logika perhitungan tetap sama
        modal_pokok = sum(item["total"] for item in self.controller.bahan_pokok)
        modal_penunjang = sum(item["total"] for item in self.controller.bahan_penunjang)
        total_modal = modal_pokok + modal_penunjang
        
        self.modal_pokok_label.config(text=f"Modal Pokok: Rp {modal_pokok:,.2f}")
        self.modal_penunjang_label.config(text=f"Modal Penunjang: Rp {modal_penunjang:,.2f}")
        self.total_modal_label.config(text=f"Total Modal Keseluruhan: Rp {total_modal:,.2f}")
        
        # Reset hasil perhitungan lainnya
        self.total_pemasukan_label.config(text="Total Pemasukan: Rp 0")
        self.margin_label.config(text="Margin: 0.00%", bootstyle="warning") 
        self.hasil_label.config(text="Status: -", bootstyle="default") # Menggunakan warna default tema

    def hitung_laba_rugi(self):
        try:
            harga_jual = float(self.harga_jual_entry.get())
            jumlah_terjual = int(self.jumlah_terjual_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Input Harga Jual dan Jumlah Terjual harus berupa angka!")
            return

        modal_pokok = sum(item["total"] for item in self.controller.bahan_pokok)
        modal_penunjang = sum(item["total"] for item in self.controller.bahan_penunjang)
        total_modal = modal_pokok + modal_penunjang
        
        total_pemasukan = harga_jual * jumlah_terjual
        hasil = total_pemasukan - total_modal
        margin = (hasil / total_pemasukan) * 100 if total_pemasukan > 0 else 0

        # Update semua label hasil
        self.total_pemasukan_label.config(text=f"Total Pemasukan: Rp {total_pemasukan:,.2f}")
        self.margin_label.config(text=f"Margin: {margin:.2f}%")

        # Penggunaan 'bootstyle' untuk warna dinamis
        if hasil > 0:
            self.hasil_label.config(text=f"💰 UNTUNG: Rp {hasil:,.2f}", bootstyle="success") # Hijau
        elif hasil < 0:
            self.hasil_label.config(text=f"🚨 RUGI: Rp {abs(hasil):,.2f}", bootstyle="danger") # Merah
        else:
            self.hasil_label.config(text="⚖️ IMPAS (BEP)", bootstyle="info") # Biru/Cyan


# ==============================================================================
# BAGIAN UNTUK MENJALANKAN APLIKASI
# ==============================================================================
if __name__ == "__main__":
    app = AplikasiBisnis()
    app.mainloop()