import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

class AdvancedProfitCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Galcalbu")
        self.root.geometry("1200x800")
        
        # Setup database
        self.setup_database()
        
        # Memuat daftar proyek dari database saat aplikasi dimulai
        self.load_projects_list_from_db()
        
        # Jika tidak ada proyek sama sekali, buat satu proyek default
        if not self.projects:
            self.current_project = "Project Utama"
            self.projects.append(self.current_project)
            self.cursor.execute("INSERT INTO projects (name, created_date) VALUES (?, ?)", 
                                (self.current_project, datetime.now().strftime("%Y-%m-%d")))
            self.conn.commit()
        else:
            self.current_project = self.projects[0]

        # Data storage (akan diisi dari database)
        self.main_items = []
        self.support_items = []
        self.sales_history = []
        
        # Load settings
        self.settings = self.load_settings()
        
        # Style configuration - HARUS dilakukan sebelum membuat interface
        self.setup_styles()
        
        self.create_main_interface()
        
    def setup_database(self):
        self.conn = sqlite3.connect('profit_calculator.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, created_date TEXT
            )''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS main_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, name TEXT,
                price REAL, quantity INTEGER, total REAL, category TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS support_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, name TEXT,
                price REAL, quantity INTEGER, total REAL, category TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, selling_price REAL,
                profit REAL, margin REAL, date TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )''')
        self.conn.commit()
    
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        # Default settings
        return {
            "currency": "Rp",
            "date_format": "%d-%m-%Y",
            "auto_backup": True,
            "backup_path": "",
            "theme": "light"
        }
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except:
            return False
    
    def load_projects_list_from_db(self):
        self.cursor.execute("SELECT name FROM projects")
        projects_tuples = self.cursor.fetchall()
        self.projects = [project[0] for project in projects_tuples]

    def get_current_project_id(self):
        self.cursor.execute("SELECT id FROM projects WHERE name = ?", (self.current_project,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def setup_styles(self):
        """Setup styles based on current theme"""
        self.style = ttk.Style()
        
        if self.settings['theme'] == 'dark':
            # Dark theme colors
            self.bg_color = '#2c3e50'
            self.card_bg = '#34495e'
            self.text_color = '#ecf0f1'
            self.accent_color = '#3498db'
            self.style.theme_use('clam')
            
            # Configure styles for dark theme
            self.style.configure('.', background=self.bg_color, foreground=self.text_color)
            self.style.configure('Main.TFrame', background=self.bg_color)
            self.style.configure('Card.TFrame', background=self.card_bg, relief='raised', borderwidth=1)
            self.style.configure('Title.TLabel', background=self.bg_color, foreground=self.text_color, font=('Arial', 16, 'bold'))
            self.style.configure('Metric.TLabel', background=self.card_bg, foreground=self.text_color, font=('Arial', 11, 'bold'))
            self.style.configure('TButton', background=self.card_bg, foreground=self.text_color)
            self.style.configure('TEntry', fieldbackground=self.card_bg, foreground=self.text_color)
            self.style.configure('TCombobox', fieldbackground=self.card_bg, foreground=self.text_color)
            self.style.configure('Treeview', background=self.card_bg, foreground=self.text_color, fieldbackground=self.card_bg)
            self.style.configure('Treeview.Heading', background=self.bg_color, foreground=self.text_color)
            
        else:
            # Light theme colors (default)
            self.bg_color = '#2c3e50'
            self.card_bg = '#ecf0f1'
            self.text_color = '#2c3e50'
            self.accent_color = '#3498db'
            self.style.theme_use('clam')
            
            # Configure styles for light theme
            self.style.configure('Main.TFrame', background=self.bg_color)
            self.style.configure('Card.TFrame', background=self.card_bg, relief='raised', borderwidth=1)
            self.style.configure('Title.TLabel', background=self.bg_color, foreground='white', font=('Arial', 16, 'bold'))
            self.style.configure('Metric.TLabel', background=self.card_bg, foreground=self.text_color, font=('Arial', 11, 'bold'))
        
        # Configure root window background
        self.root.configure(bg=self.bg_color)

    def apply_theme(self):
        """Apply current theme to all widgets"""
        self.setup_styles()
        
        # Update all existing widgets
        self.update_widget_colors(self.root)
        
        # Refresh UI to reflect theme changes
        self.refresh_ui()

    def update_widget_colors(self, widget):
        """Recursively update colors for all widgets"""
        try:
            if isinstance(widget, (ttk.Frame, ttk.LabelFrame)):
                if 'Card' in str(widget.configure('style')):
                    widget.configure(style='Card.TFrame')
                else:
                    widget.configure(style='Main.TFrame')
            elif isinstance(widget, ttk.Label):
                if 'Title' in str(widget.configure('style')):
                    widget.configure(style='Title.TLabel')
                else:
                    widget.configure(style='Metric.TLabel')
            elif isinstance(widget, ttk.Button):
                widget.configure(style='TButton')
            elif isinstance(widget, ttk.Entry):
                widget.configure(style='TEntry')
            elif isinstance(widget, ttk.Combobox):
                widget.configure(style='TCombobox')
            elif isinstance(widget, ttk.Treeview):
                widget.configure(style='Treeview')
        except:
            pass
        
        # Recursively update child widgets
        for child in widget.winfo_children():
            self.update_widget_colors(child)

    def create_main_interface(self):
        main_container = ttk.Frame(self.root, style='Main.TFrame')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_header(main_container)
        
        content_frame = ttk.Frame(main_container, style='Main.TFrame')
        content_frame.pack(fill='both', expand=True, pady=10)
        
        self.create_sidebar(content_frame)
        self.create_main_content(content_frame)
        
        self.load_project_data()

    def create_header(self, parent):
        header_frame = ttk.Frame(parent, style='Main.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="KALKULATOR UNTUNG RUGI", style='Title.TLabel')
        title_label.pack(side='left')
        
        project_frame = ttk.Frame(header_frame, style='Main.TFrame')
        project_frame.pack(side='right')
        
        ttk.Label(project_frame, text="Project:", style='Metric.TLabel').pack(side='left', padx=5)
        self.project_var = tk.StringVar(value=self.current_project)
        self.project_combo = ttk.Combobox(project_frame, textvariable=self.project_var, values=self.projects, width=15)
        self.project_combo.pack(side='left', padx=5)
        self.project_combo.bind('<<ComboboxSelected>>', self.on_project_change)
        
        ttk.Button(project_frame, text="+ Project", command=self.create_new_project).pack(side='left', padx=5)

    def create_sidebar(self, parent):
        self.sidebar_frame = ttk.Frame(parent, width=250, style='Main.TFrame')
        self.sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        self.sidebar_frame.pack_propagate(False)
        
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("📦 Barang Pokok", lambda: self.show_items_page("main")),
            ("🛠️ Barang Penunjang", lambda: self.show_items_page("support")),
            ("💰 Hitung Keuntungan", self.calculate_profit),
            ("📈 Laporan", self.show_reports),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(self.sidebar_frame, text=text, command=command, width=20)
            btn.pack(pady=5, padx=10, fill='x')
        
        self.update_sidebar_stats()

    def update_sidebar_stats(self):
        for widget in self.sidebar_frame.winfo_children():
            if isinstance(widget, ttk.Frame) and hasattr(widget, 'is_stats_frame'):
                widget.destroy()

        stats_frame = ttk.Frame(self.sidebar_frame, style='Card.TFrame')
        stats_frame.is_stats_frame = True
        stats_frame.pack(fill='x', pady=20, padx=10)
        
        ttk.Label(stats_frame, text="Quick Stats", style='Metric.TLabel').pack(pady=10)
        
        total_cost = self.get_total_cost()
        total_profit = sum(sale['profit'] for sale in self.sales_history)
        avg_margin = self.get_avg_margin()
        
        ttk.Label(stats_frame, text=f"Total Biaya: {self.settings['currency']} {total_cost:,.2f}", style='Metric.TLabel').pack(anchor='w', padx=10)
        ttk.Label(stats_frame, text=f"Total Untung: {self.settings['currency']} {total_profit:,.2f}", style='Metric.TLabel').pack(anchor='w', padx=10, pady=(10,0))
        ttk.Label(stats_frame, text=f"Rata-rata Margin: {avg_margin:.2f}%", style='Metric.TLabel').pack(anchor='w', padx=10, pady=(10,0))

    def create_main_content(self, parent):
        self.main_content = ttk.Frame(parent, style='Main.TFrame')
        self.main_content.pack(side='right', fill='both', expand=True)
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_main_content()
        self.current_view = 'dashboard'
        
        title_label = ttk.Label(self.main_content, text="Dashboard Utama", style='Title.TLabel')
        title_label.pack(pady=10)
        
        metrics_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        metrics_frame.pack(fill='x', pady=10)
        
        metrics = [
            ("Total Barang Pokok", len(self.main_items), "#3498db"),
            ("Total Barang Penunjang", len(self.support_items), "#e74c3c"),
            (f"Total Biaya Produksi", f"{self.settings['currency']} {self.get_total_cost():,.2f}", "#f39c12"),
            ("Rata-rata Margin", f"{self.get_avg_margin():.1f}%", "#2ecc71")
        ]
        
        for i, (title, value, color) in enumerate(metrics):
            card = self.create_metric_card(metrics_frame, title, value, color)
            card.grid(row=0, column=i, padx=5, sticky='nsew')
            metrics_frame.columnconfigure(i, weight=1)
        
        content_frame = ttk.Frame(self.main_content, style='Main.TFrame')
        content_frame.pack(fill='both', expand=True, pady=10)
        
        chart_frame = ttk.Frame(content_frame, style='Card.TFrame')
        chart_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        ttk.Label(chart_frame, text="Distribusi Biaya", style='Metric.TLabel').pack(pady=10)
        self.create_cost_chart(chart_frame)
        
        activity_frame = ttk.Frame(content_frame, style='Card.TFrame')
        activity_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        ttk.Label(activity_frame, text="Histori Perhitungan Terbaru", style='Metric.TLabel').pack(pady=10)
        self.create_activity_list(activity_frame)

    def create_metric_card(self, parent, title, value, color):
        card = ttk.Frame(parent, style='Card.TFrame')
        ttk.Label(card, text=title, style='Metric.TLabel').pack(pady=10)
        value_label = ttk.Label(card, text=value, font=('Arial', 14, 'bold'), 
                               background=self.card_bg, foreground=color)
        value_label.pack(pady=10)
        return card

    def create_cost_chart(self, parent):
        main_total = sum(item['total'] for item in self.main_items)
        support_total = sum(item['total'] for item in self.support_items)
        
        if main_total == 0 and support_total == 0:
            label = ttk.Label(parent, text="Tidak ada data biaya untuk ditampilkan", 
                             background=self.card_bg, foreground=self.text_color)
            label.pack(pady=50)
            return
            
        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        ax.pie([main_total, support_total], labels=['Barang Pokok', 'Barang Penunjang'], 
               colors=['#3498db', '#e74c3c'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def create_activity_list(self, parent):
        if not self.sales_history:
            label = ttk.Label(parent, text="Belum ada perhitungan yang disimpan.", 
                             background=self.card_bg, foreground=self.text_color)
            label.pack(pady=20)
            return

        for sale in reversed(self.sales_history[-5:]):
            activity_frame = ttk.Frame(parent, style='Card.TFrame')
            activity_frame.pack(fill='x', padx=10, pady=5)
            
            profit_text = f"Untung: {self.settings['currency']} {sale['profit']:,.2f} (Margin: {sale['margin']:.2f}%)"
            date_text = f"Pada: {sale['date']}"
            
            ttk.Label(activity_frame, text=profit_text, style='Metric.TLabel').pack(anchor='w')
            ttk.Label(activity_frame, text=date_text, background=self.card_bg, 
                     foreground='#7f8c8d').pack(anchor='w')

    def show_items_page(self, item_type):
        self.clear_main_content()
        self.current_view = 'main_items' if item_type == 'main' else 'support_items'
        
        if item_type == "main":
            title = "Manajemen Barang Pokok"
            items_list = self.main_items
            add_command = lambda: self.add_item_dialog("main")
        else:
            title = "Manajemen Barang Penunjang"
            items_list = self.support_items
            add_command = lambda: self.add_item_dialog("support")

        title_label = ttk.Label(self.main_content, text=title, style='Title.TLabel')
        title_label.pack(pady=10)
        
        toolbar = ttk.Frame(self.main_content, style='Main.TFrame')
        toolbar.pack(fill='x', pady=10)
        
        ttk.Button(toolbar, text="+ Tambah Barang", command=add_command).pack(side='left')
        
        table_frame = ttk.Frame(self.main_content, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True)
        
        columns = ("No", "Nama Barang", "Kategori", "Harga Satuan", "Jumlah", "Total", "Aksi")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns: 
            tree.heading(col, text=col)
        tree.column("No", width=50, anchor='center')
        tree.column("Nama Barang", width=150)
        tree.column("Aksi", width=100, anchor='center')

        for i, item in enumerate(items_list, 1):
            item_id = item.get('id', i)
            tree.insert("", "end", iid=item_id, values=(
                i, item['name'], item.get('category', '-'), 
                f"{self.settings['currency']} {item['price']:,.2f}", 
                item['quantity'], 
                f"{self.settings['currency']} {item['total']:,.2f}",
                "Edit/Hapus"
            ))
        
        # Add edit/delete functionality
        def on_item_action(event):
            item_id = tree.identify_row(event.y)
            if item_id:
                column = tree.identify_column(event.x)
                if column == "#7":  # Aksi column
                    self.item_action_dialog(item_type, int(item_id))
        
        tree.bind("<Button-1>", on_item_action)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

    def item_action_dialog(self, item_type, item_id):
        """Dialog untuk edit atau hapus item"""
        if item_type == "main":
            items = self.main_items
            table_name = "main_items"
        else:
            items = self.support_items
            table_name = "support_items"
        
        # Find the item
        item = None
        for it in items:
            if it.get('id') == item_id:
                item = it
                break
        
        if not item:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit/Hapus Barang")
        dialog.geometry("300x150")
        dialog.configure(bg=self.card_bg)
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, style='Card.TFrame')
        frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        ttk.Label(frame, text=f"Barang: {item['name']}", background=self.card_bg, 
                 foreground=self.text_color, font=('Arial', 11, 'bold')).pack(pady=10)
        
        def edit_item():
            dialog.destroy()
            self.edit_item_dialog(item_type, item_id)
        
        def delete_item():
            if messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus {item['name']}?", parent=dialog):
                project_id = self.get_current_project_id()
                self.cursor.execute(f"DELETE FROM {table_name} WHERE id = ? AND project_id = ?", (item_id, project_id))
                self.conn.commit()
                dialog.destroy()
                self.load_project_data()
                self.show_items_page(item_type)
        
        ttk.Button(frame, text="Edit Barang", command=edit_item).pack(pady=5, fill='x')
        ttk.Button(frame, text="Hapus Barang", command=delete_item).pack(pady=5, fill='x')

    def edit_item_dialog(self, item_type, item_id):
        """Dialog untuk mengedit item"""
        if item_type == "main":
            items = self.main_items
            table_name = "main_items"
        else:
            items = self.support_items
            table_name = "support_items"
        
        # Find the item
        item = None
        for it in items:
            if it.get('id') == item_id:
                item = it
                break
        
        if not item:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Barang")
        dialog.geometry("350x250")
        dialog.configure(bg=self.card_bg)
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, style='Card.TFrame')
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        labels = ["Nama Barang:", "Kategori:", "Harga Satuan:", "Jumlah:"]
        entries = {}

        for i, text in enumerate(labels):
            ttk.Label(frame, text=text, background=self.card_bg, 
                     foreground=self.text_color).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
            entries[text] = entry

        # Pre-fill with current values
        entries["Nama Barang:"].insert(0, item['name'])
        entries["Kategori:"].insert(0, item.get('category', ''))
        entries["Harga Satuan:"].insert(0, str(item['price']))
        entries["Jumlah:"].insert(0, str(item['quantity']))

        def save_edited_item():
            try:
                name = entries["Nama Barang:"].get()
                price = float(entries["Harga Satuan:"].get())
                quantity = int(entries["Jumlah:"].get())
                category = entries["Kategori:"].get()
                
                if not name or price <= 0 or quantity <= 0:
                    messagebox.showerror("Input Tidak Valid", "Nama, harga, dan jumlah harus diisi dengan benar.", parent=dialog)
                    return

                project_id = self.get_current_project_id()
                total = price * quantity
                
                self.cursor.execute(f'''
                    UPDATE {table_name} 
                    SET name=?, price=?, quantity=?, total=?, category=?
                    WHERE id=? AND project_id=?
                ''', (name, price, quantity, total, category, item_id, project_id))
                self.conn.commit()

                dialog.destroy()
                self.load_project_data()
                self.show_items_page(item_type)
            
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah harus berupa angka.", parent=dialog)

        ttk.Button(frame, text="Simpan Perubahan", command=save_edited_item).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def calculate_profit(self):
        self.clear_main_content()
        self.current_view = 'profit'
        
        title_label = ttk.Label(self.main_content, text="Kalkulator Keuntungan", style='Title.TLabel')
        title_label.pack(pady=10)
        
        form_frame = ttk.Frame(self.main_content, style='Card.TFrame')
        form_frame.pack(fill='x', pady=10, padx=20)
        
        ttk.Label(form_frame, text="Harga Jual Produk:", style='Metric.TLabel').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        selling_price_entry = ttk.Entry(form_frame, width=20, font=('Arial', 12))
        selling_price_entry.grid(row=0, column=1, padx=10, pady=10)
        
        results_container = ttk.Frame(self.main_content, style='Main.TFrame')
        results_container.pack(fill='x', padx=20)

        def calculate():
            for widget in results_container.winfo_children(): 
                widget.destroy()

            try:
                selling_price = float(selling_price_entry.get())
                total_cost = self.get_total_cost()
                
                if selling_price <= 0:
                     messagebox.showerror("Error", "Harga jual harus lebih dari 0")
                     return
                
                profit = selling_price - total_cost
                margin = (profit / selling_price) * 100 if selling_price != 0 else 0
                
                results_frame = ttk.Frame(results_container, style='Card.TFrame')
                results_frame.pack(fill='x', pady=10)
                
                results_text = f"HASIL PERHITUNGAN:\n\n" \
                               f"Total Biaya Produksi: {self.settings['currency']} {total_cost:,.2f}\n" \
                               f"Harga Jual: {self.settings['currency']} {selling_price:,.2f}\n" \
                               f"Keuntungan: {self.settings['currency']} {profit:,.2f}\n" \
                               f"Margin: {margin:.2f}%"
                
                ttk.Label(results_frame, text=results_text, style='Metric.TLabel', font=('Arial', 11), justify='left').pack(pady=20, anchor='w', padx=10)
                
                self.save_calculation(selling_price, profit, margin)
                
            except ValueError:
                messagebox.showerror("Error", "Masukkan angka yang valid untuk harga jual")
        
        ttk.Button(form_frame, text="Hitung Keuntungan", command=calculate).grid(row=2, column=0, columnspan=2, pady=20)

    def show_reports(self):
        self.clear_main_content()
        self.current_view = 'reports'
        
        title_label = ttk.Label(self.main_content, text="Laporan dan Analisis", style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Create notebook for different report types
        notebook = ttk.Notebook(self.main_content)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sales Report Tab
        sales_frame = ttk.Frame(notebook, style='Card.TFrame')
        notebook.add(sales_frame, text="Laporan Penjualan")
        self.create_sales_report(sales_frame)
        
        # Items Report Tab
        items_frame = ttk.Frame(notebook, style='Card.TFrame')
        notebook.add(items_frame, text="Laporan Barang")
        self.create_items_report(items_frame)
        
        # Export Frame
        export_frame = ttk.Frame(self.main_content, style='Card.TFrame')
        export_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(export_frame, text="Export Laporan ke CSV", command=self.export_report).pack(pady=10)

    def create_sales_report(self, parent):
        if not self.sales_history:
            ttk.Label(parent, text="Belum ada data penjualan.", 
                     background=self.card_bg, foreground=self.text_color).pack(pady=50)
            return
        
        columns = ("No", "Tanggal", "Harga Jual", "Keuntungan", "Margin")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        for col in columns: 
            tree.heading(col, text=col)
        
        for i, sale in enumerate(self.sales_history, 1):
            tree.insert("", "end", values=(
                i, 
                sale['date'], 
                f"{self.settings['currency']} {sale['selling_price']:,.2f}",
                f"{self.settings['currency']} {sale['profit']:,.2f}",
                f"{sale['margin']:.2f}%"
            ))
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Summary
        total_sales = sum(sale['selling_price'] for sale in self.sales_history)
        total_profit = sum(sale['profit'] for sale in self.sales_history)
        avg_margin = self.get_avg_margin()
        
        summary_frame = ttk.Frame(parent, style='Card.TFrame')
        summary_frame.pack(fill='x', padx=10, pady=10)
        
        summary_text = f"Total Penjualan: {self.settings['currency']} {total_sales:,.2f} | " \
                      f"Total Keuntungan: {self.settings['currency']} {total_profit:,.2f} | " \
                      f"Rata-rata Margin: {avg_margin:.2f}%"
        
        ttk.Label(summary_frame, text=summary_text, style='Metric.TLabel').pack(pady=5)

    def create_items_report(self, parent):
        # Main items report
        main_frame = ttk.LabelFrame(parent, text="Barang Pokok", style='Card.TFrame')
        main_frame.pack(fill='x', padx=10, pady=5)
        
        if self.main_items:
            columns = ("No", "Nama Barang", "Kategori", "Harga", "Jumlah", "Total")
            tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
            
            for col in columns: 
                tree.heading(col, text=col)
            
            for i, item in enumerate(self.main_items, 1):
                tree.insert("", "end", values=(
                    i, item['name'], item.get('category', '-'),
                    f"{self.settings['currency']} {item['price']:,.2f}",
                    item['quantity'],
                    f"{self.settings['currency']} {item['total']:,.2f}"
                ))
            
            tree.pack(fill='both', expand=True, padx=10, pady=10)
        else:
            ttk.Label(main_frame, text="Tidak ada barang pokok.", 
                     background=self.card_bg, foreground=self.text_color).pack(pady=20)
        
        # Support items report
        support_frame = ttk.LabelFrame(parent, text="Barang Penunjang", style='Card.TFrame')
        support_frame.pack(fill='x', padx=10, pady=5)
        
        if self.support_items:
            columns = ("No", "Nama Barang", "Kategori", "Harga", "Jumlah", "Total")
            tree = ttk.Treeview(support_frame, columns=columns, show="headings", height=8)
            
            for col in columns: 
                tree.heading(col, text=col)
            
            for i, item in enumerate(self.support_items, 1):
                tree.insert("", "end", values=(
                    i, item['name'], item.get('category', '-'),
                    f"{self.settings['currency']} {item['price']:,.2f}",
                    item['quantity'],
                    f"{self.settings['currency']} {item['total']:,.2f}"
                ))
            
            tree.pack(fill='both', expand=True, padx=10, pady=10)
        else:
            ttk.Label(support_frame, text="Tidak ada barang penunjang.", 
                     background=self.card_bg, foreground=self.text_color).pack(pady=20)

    def export_report(self):
        """Export report to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    # Write sales data
                    f.write("LAPORAN PENJUALAN\n")
                    f.write("No,Tanggal,Harga Jual,Keuntungan,Margin\n")
                    for i, sale in enumerate(self.sales_history, 1):
                        f.write(f"{i},{sale['date']},{sale['selling_price']},{sale['profit']},{sale['margin']}\n")
                    
                    f.write("\nLAPORAN BARANG POKOK\n")
                    f.write("No,Nama Barang,Kategori,Harga,Jumlah,Total\n")
                    for i, item in enumerate(self.main_items, 1):
                        f.write(f"{i},{item['name']},{item.get('category', '-')},{item['price']},{item['quantity']},{item['total']}\n")
                    
                    f.write("\nLAPORAN BARANG PENUNJANG\n")
                    f.write("No,Nama Barang,Kategori,Harga,Jumlah,Total\n")
                    for i, item in enumerate(self.support_items, 1):
                        f.write(f"{i},{item['name']},{item.get('category', '-')},{item['price']},{item['quantity']},{item['total']}\n")
                
                messagebox.showinfo("Sukses", f"Laporan berhasil diexport ke {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengexport laporan: {str(e)}")

    def show_settings(self):
        self.clear_main_content()
        self.current_view = 'settings'
        
        title_label = ttk.Label(self.main_content, text="Pengaturan", style='Title.TLabel')
        title_label.pack(pady=10)
        
        settings_frame = ttk.Frame(self.main_content, style='Card.TFrame')
        settings_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Currency setting
        currency_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        currency_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(currency_frame, text="Mata Uang:", background=self.card_bg, 
                 foreground=self.text_color).pack(side='left')
        currency_var = tk.StringVar(value=self.settings['currency'])
        currency_combo = ttk.Combobox(currency_frame, textvariable=currency_var, 
                                     values=["Rp", "$", "€", "£", "¥"], width=10)
        currency_combo.pack(side='left', padx=10)
        
        # Auto backup setting
        backup_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        backup_frame.pack(fill='x', padx=10, pady=10)
        
        backup_var = tk.BooleanVar(value=self.settings['auto_backup'])
        ttk.Checkbutton(backup_frame, text="Auto Backup", variable=backup_var, 
                       style='Card.TCheckbutton').pack(side='left')
        
        # Theme setting
        theme_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        theme_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(theme_frame, text="Tema:", background=self.card_bg, 
                 foreground=self.text_color).pack(side='left')
        theme_var = tk.StringVar(value=self.settings['theme'])
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, 
                                  values=["light", "dark"], width=10)
        theme_combo.pack(side='left', padx=10)
        
        def save_settings():
            self.settings['currency'] = currency_var.get()
            self.settings['auto_backup'] = backup_var.get()
            self.settings['theme'] = theme_var.get()
            
            if self.save_settings():
                messagebox.showinfo("Sukses", "Pengaturan berhasil disimpan")
                self.apply_theme()  # Apply theme changes
            else:
                messagebox.showerror("Error", "Gagal menyimpan pengaturan")
        
        ttk.Button(settings_frame, text="Simpan Pengaturan", command=save_settings).pack(pady=20)
        
        # Backup section
        backup_manual_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        backup_manual_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(backup_manual_frame, text="Backup Data Sekarang", 
                  command=self.manual_backup).pack(side='left', padx=5)
        ttk.Button(backup_manual_frame, text="Restore Data", 
                  command=self.restore_backup).pack(side='left', padx=5)

    def manual_backup(self):
        """Create manual backup of database"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".backup",
            filetypes=[("Backup files", "*.backup"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Copy database file
                import shutil
                shutil.copy2('profit_calculator.db', filename)
                messagebox.showinfo("Sukses", f"Backup berhasil dibuat: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membuat backup: {str(e)}")

    def restore_backup(self):
        """Restore database from backup"""
        filename = filedialog.askopenfilename(
            filetypes=[("Backup files", "*.backup"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import shutil
                # Close current database connection
                self.conn.close()
                # Replace database file
                shutil.copy2(filename, 'profit_calculator.db')
                # Reopen database connection
                self.setup_database()
                self.load_projects_list_from_db()
                self.load_project_data()
                messagebox.showinfo("Sukses", "Backup berhasil direstore")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal restore backup: {str(e)}")
                # Try to reconnect to database
                self.setup_database()

    def clear_main_content(self):
        for widget in self.main_content.winfo_children(): 
            widget.destroy()

    def get_total_cost(self):
        main_total = sum(item['total'] for item in self.main_items)
        support_total = sum(item['total'] for item in self.support_items)
        return main_total + support_total

    def get_avg_margin(self):
        if not self.sales_history: 
            return 0
        return sum(sale['margin'] for sale in self.sales_history) / len(self.sales_history)
    
    def add_item_dialog(self, item_type):
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Barang Baru")
        dialog.geometry("350x250")
        dialog.configure(bg=self.card_bg)
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, style='Card.TFrame')
        frame.pack(expand=True, fill='both', padx=10, pady=10)

        labels = ["Nama Barang:", "Kategori:", "Harga Satuan:", "Jumlah:"]
        entries = {}

        for i, text in enumerate(labels):
            ttk.Label(frame, text=text, background=self.card_bg, 
                     foreground=self.text_color).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
            entries[text] = entry

        def save_item():
            try:
                name = entries["Nama Barang:"].get()
                price = float(entries["Harga Satuan:"].get())
                quantity = int(entries["Jumlah:"].get())
                category = entries["Kategori:"].get()
                
                if not name or price <= 0 or quantity <= 0:
                    messagebox.showerror("Input Tidak Valid", "Nama, harga, dan jumlah harus diisi dengan benar.", parent=dialog)
                    return

                project_id = self.get_current_project_id()
                table_name = "main_items" if item_type == "main" else "support_items"
                
                self.cursor.execute(f'''
                    INSERT INTO {table_name} (project_id, name, price, quantity, total, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (project_id, name, price, quantity, price * quantity, category))
                self.conn.commit()

                dialog.destroy()
                self.load_project_data()
                self.show_items_page(item_type)
            
            except ValueError:
                messagebox.showerror("Error", "Harga dan Jumlah harus berupa angka.", parent=dialog)

        ttk.Button(frame, text="Simpan", command=save_item).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def save_calculation(self, selling_price, profit, margin):
        project_id = self.get_current_project_id()
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute('''
            INSERT INTO sales (project_id, selling_price, profit, margin, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, selling_price, profit, margin, date_str))
        self.conn.commit()
        
        self.load_project_data()

    def create_new_project(self):
        project_name = simpledialog.askstring("Project Baru", "Masukkan nama project:", parent=self.root)
        if project_name and project_name not in self.projects:
            try:
                self.cursor.execute("INSERT INTO projects (name, created_date) VALUES (?, ?)", 
                                    (project_name, datetime.now().strftime("%Y-%m-%d")))
                self.conn.commit()

                self.projects.append(project_name)
                self.project_combo['values'] = self.projects
                self.project_var.set(project_name)
                self.on_project_change(None) 
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Nama project sudah ada.")

    def on_project_change(self, event):
        self.current_project = self.project_var.get()
        self.load_project_data()
    
    def load_project_data(self):
        project_id = self.get_current_project_id()
        if not project_id: 
            return

        # Memuat barang pokok dengan ID
        self.cursor.execute("SELECT id, name, price, quantity, total, category FROM main_items WHERE project_id = ?", (project_id,))
        self.main_items = [{'id': r[0], 'name': r[1], 'price': r[2], 'quantity': r[3], 'total': r[4], 'category': r[5]} for r in self.cursor.fetchall()]

        # Memuat barang penunjang dengan ID
        self.cursor.execute("SELECT id, name, price, quantity, total, category FROM support_items WHERE project_id = ?", (project_id,))
        self.support_items = [{'id': r[0], 'name': r[1], 'price': r[2], 'quantity': r[3], 'total': r[4], 'category': r[5]} for r in self.cursor.fetchall()]

        # Memuat histori penjualan
        self.cursor.execute("SELECT selling_price, profit, margin, date FROM sales WHERE project_id = ?", (project_id,))
        self.sales_history = [{'selling_price': r[0], 'profit': r[1], 'margin': r[2], 'date': r[3]} for r in self.cursor.fetchall()]
        
        self.refresh_ui()

    def refresh_ui(self):
        self.update_sidebar_stats()
        # Keep current view or go to dashboard
        current_view = getattr(self, 'current_view', 'dashboard')
        if current_view == 'dashboard':
            self.show_dashboard()
        elif current_view == 'main_items':
            self.show_items_page("main")
        elif current_view == 'support_items':
            self.show_items_page("support")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedProfitCalculator(root)
    root.mainloop()