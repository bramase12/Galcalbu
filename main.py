import tkinter as tk
from tkinter import ttk, messagebox

class ProfitCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Galcalbu")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.main_items = []
        self.support_items = []
        
        self.create_main_menu()
        
    def create_main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Title
        title_label = tk.Label(self.root, text="MENU UTAMA", font=("Arial", 16, "bold"), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        btn1 = tk.Button(button_frame, text="LIST HARGA BARANG POKOK & PENUNJANG", 
                        command=self.show_price_list, width=40, height=2,
                        bg='#3498db', fg='white', font=("Arial", 10))
        btn1.grid(row=0, column=0, padx=10, pady=10)
        
        btn2 = tk.Button(button_frame, text="HITUNG TOTAL HARGA POKOK & HARGA SATUAN & LABA & KEUNTUNGAN", 
                        command=self.calculate_profit, width=40, height=2,
                        bg='#2ecc71', fg='white', font=("Arial", 10))
        btn2.grid(row=1, column=0, padx=10, pady=10)
        
        # Display summary
        summary_frame = tk.Frame(self.root, bg='#f0f0f0')
        summary_frame.pack(pady=20)
        
        # Total Harga Bahan Pokok
        self.main_total_label = tk.Label(summary_frame, text="TOTAL HARGA BAHAN POKOK: Rp 0", 
                                        font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#e74c3c')
        self.main_total_label.grid(row=0, column=0, padx=20, pady=5)
        
        # Total Harga Penunjang
        self.support_total_label = tk.Label(summary_frame, text="TOTAL HARGA PENUNJANG/LAINNYA: Rp 0", 
                                           font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#e74c3c')
        self.support_total_label.grid(row=1, column=0, padx=20, pady=5)
        
        # Pendapatan
        self.income_label = tk.Label(summary_frame, text="PENDAPATAN: Rp 0", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#27ae60')
        self.income_label.grid(row=2, column=0, padx=20, pady=5)
        
        # Margin
        self.margin_label = tk.Label(summary_frame, text="MARGIN: 0%", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#f39c12')
        self.margin_label.grid(row=3, column=0, padx=20, pady=5)
        
        # Keuntungan
        self.profit_label = tk.Label(summary_frame, text="KEUNTUNGAN: Rp 0", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#27ae60')
        self.profit_label.grid(row=4, column=0, padx=20, pady=5)
        
        self.update_summary()
        
    def show_price_list(self):
        # Create new window for price list
        price_window = tk.Toplevel(self.root)
        price_window.title("List Harga Barang")
        price_window.geometry("900x500")
        price_window.configure(bg='#f0f0f0')
        
        # Notebook for tabs
        notebook = ttk.Notebook(price_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab for main items
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="TABEL HARGA POKOK")
        
        # Table for main items
        main_tree = ttk.Treeview(main_frame, columns=("Nama", "Harga", "Jumlah", "Total"), show="headings")
        main_tree.heading("Nama", text="Nama Barang")
        main_tree.heading("Harga", text="Harga Satuan")
        main_tree.heading("Jumlah", text="Jumlah")
        main_tree.heading("Total", text="Total Harga")
        main_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Form to add main items
        add_main_frame = tk.Frame(main_frame, bg='#f0f0f0')
        add_main_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(add_main_frame, text="Nama Barang:", bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5)
        main_name_entry = tk.Entry(add_main_frame, width=20)
        main_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_main_frame, text="Harga Satuan:", bg='#f0f0f0').grid(row=0, column=2, padx=5, pady=5)
        main_price_entry = tk.Entry(add_main_frame, width=15)
        main_price_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_main_frame, text="Jumlah:", bg='#f0f0f0').grid(row=0, column=4, padx=5, pady=5)
        main_qty_entry = tk.Entry(add_main_frame, width=10)
        main_qty_entry.grid(row=0, column=5, padx=5, pady=5)
        
        def add_main_item():
            name = main_name_entry.get()
            try:
                price = int(main_price_entry.get())
                qty = int(main_qty_entry.get())
                total = price * qty
                
                self.main_items.append({
                    "name": name,
                    "price": price,
                    "quantity": qty,
                    "total": total
                })
                
                main_tree.insert("", "end", values=(name, f"Rp {price:,}", qty, f"Rp {total:,}"))
                
                # Clear entries
                main_name_entry.delete(0, tk.END)
                main_price_entry.delete(0, tk.END)
                main_qty_entry.delete(0, tk.END)
                
                self.update_summary()
                
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah harus berupa angka")
        
        add_main_btn = tk.Button(add_main_frame, text="Tambah Barang Pokok", 
                                command=add_main_item, bg='#3498db', fg='white')
        add_main_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # Tab for support items
        support_frame = ttk.Frame(notebook)
        notebook.add(support_frame, text="TABEL HARGA PENUNJANG")
        
        # Table for support items
        support_tree = ttk.Treeview(support_frame, columns=("Nama", "Harga", "Jumlah", "Total"), show="headings")
        support_tree.heading("Nama", text="Nama Barang")
        support_tree.heading("Harga", text="Harga Satuan")
        support_tree.heading("Jumlah", text="Jumlah")
        support_tree.heading("Total", text="Total Harga")
        support_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Form to add support items
        add_support_frame = tk.Frame(support_frame, bg='#f0f0f0')
        add_support_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(add_support_frame, text="Nama Barang:", bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5)
        support_name_entry = tk.Entry(add_support_frame, width=20)
        support_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_support_frame, text="Harga Satuan:", bg='#f0f0f0').grid(row=0, column=2, padx=5, pady=5)
        support_price_entry = tk.Entry(add_support_frame, width=15)
        support_price_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_support_frame, text="Jumlah:", bg='#f0f0f0').grid(row=0, column=4, padx=5, pady=5)
        support_qty_entry = tk.Entry(add_support_frame, width=10)
        support_qty_entry.grid(row=0, column=5, padx=5, pady=5)
        
        def add_support_item():
            name = support_name_entry.get()
            try:
                price = int(support_price_entry.get())
                qty = int(support_qty_entry.get())
                total = price * qty
                
                self.support_items.append({
                    "name": name,
                    "price": price,
                    "quantity": qty,
                    "total": total
                })
                
                support_tree.insert("", "end", values=(name, f"Rp {price:,}", qty, f"Rp {total:,}"))
                
                # Clear entries
                support_name_entry.delete(0, tk.END)
                support_price_entry.delete(0, tk.END)
                support_qty_entry.delete(0, tk.END)
                
                self.update_summary()
                
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah harus berupa angka")
        
        add_support_btn = tk.Button(add_support_frame, text="Tambah Barang Penunjang", 
                                   command=add_support_item, bg='#3498db', fg='white')
        add_support_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # Populate existing items
        for item in self.main_items:
            main_tree.insert("", "end", values=(
                item["name"], 
                f"Rp {item['price']:,}", 
                item["quantity"], 
                f"Rp {item['total']:,}"
            ))
            
        for item in self.support_items:
            support_tree.insert("", "end", values=(
                item["name"], 
                f"Rp {item['price']:,}", 
                item["quantity"], 
                f"Rp {item['total']:,}"
            ))
    
    def calculate_profit(self):
        # Create new window for profit calculation
        profit_window = tk.Toplevel(self.root)
        profit_window.title("Hitung Keuntungan")
        profit_window.geometry("500x400")
        profit_window.configure(bg='#f0f0f0')
        
        # Form for selling price
        form_frame = tk.Frame(profit_window, bg='#f0f0f0')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="FORM HARGA JUAL", font=("Arial", 14, "bold"), 
                bg='#f0f0f0', fg='#2c3e50').grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(form_frame, text="Harga Jual:", bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=10, sticky='e')
        selling_price_entry = tk.Entry(form_frame, width=20)
        selling_price_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Calculate button
        def calculate():
            try:
                selling_price = int(selling_price_entry.get())
                
                # Calculate totals
                main_total = sum(item["total"] for item in self.main_items)
                support_total = sum(item["total"] for item in self.support_items)
                total_cost = main_total + support_total
                
                # Calculate profit
                profit = selling_price - total_cost
                margin = (profit / selling_price) * 100 if selling_price > 0 else 0
                
                # Display results
                result_frame = tk.Frame(profit_window, bg='#f0f0f0')
                result_frame.pack(pady=20)
                
                tk.Label(result_frame, text="HASIL PERHITUNGAN", font=("Arial", 12, "bold"), 
                        bg='#f0f0f0', fg='#2c3e50').grid(row=0, column=0, columnspan=2, pady=10)
                
                tk.Label(result_frame, text="TOTAL BIAYA:", bg='#f0f0f0', font=("Arial", 10)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
                tk.Label(result_frame, text=f"Rp {total_cost:,}", bg='#f0f0f0', font=("Arial", 10, "bold")).grid(row=1, column=1, sticky='w', padx=5, pady=5)
                
                tk.Label(result_frame, text="HARGA JUAL:", bg='#f0f0f0', font=("Arial", 10)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
                tk.Label(result_frame, text=f"Rp {selling_price:,}", bg='#f0f0f0', font=("Arial", 10, "bold")).grid(row=2, column=1, sticky='w', padx=5, pady=5)
                
                tk.Label(result_frame, text="KEUNTUNGAN:", bg='#f0f0f0', font=("Arial", 10)).grid(row=3, column=0, sticky='e', padx=5, pady=5)
                profit_color = '#27ae60' if profit >= 0 else '#e74c3c'
                tk.Label(result_frame, text=f"Rp {profit:,}", bg='#f0f0f0', font=("Arial", 10, "bold"), fg=profit_color).grid(row=3, column=1, sticky='w', padx=5, pady=5)
                
                tk.Label(result_frame, text="MARGIN:", bg='#f0f0f0', font=("Arial", 10)).grid(row=4, column=0, sticky='e', padx=5, pady=5)
                margin_color = '#27ae60' if margin >= 0 else '#e74c3c'
                tk.Label(result_frame, text=f"{margin:.2f}%", bg='#f0f0f0', font=("Arial", 10, "bold"), fg=margin_color).grid(row=4, column=1, sticky='w', padx=5, pady=5)
                
            except ValueError:
                messagebox.showerror("Error", "Harga Jual harus berupa angka")
        
        calc_btn = tk.Button(form_frame, text="Hitung Keuntungan", command=calculate, 
                            bg='#2ecc71', fg='white', font=("Arial", 10))
        calc_btn.grid(row=2, column=0, columnspan=2, pady=20)
    
    def update_summary(self):
        # Calculate totals
        main_total = sum(item["total"] for item in self.main_items)
        support_total = sum(item["total"] for item in self.support_items)
        total_cost = main_total + support_total
        
        # Update labels
        self.main_total_label.config(text=f"TOTAL HARGA BAHAN POKOK: Rp {main_total:,}")
        self.support_total_label.config(text=f"TOTAL HARGA PENUNJANG/LAINNYA: Rp {support_total:,}")
        
        # For now, we'll set income to 0 until calculated in profit window
        # In a real app, you might want to store the selling price and update this
        
        # Update main window with latest data
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfitCalculatorApp(root)
    root.mainloop()