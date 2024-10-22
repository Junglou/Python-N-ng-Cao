import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Menu
import psycopg2

class Login:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng Nhập")
        self.master.geometry("350x220")
        self.master.configure(bg="#f0f0f0")

        self.title_label = tk.Label(self.master, text="ĐĂNG NHẬP", font=("Times New Roman", 24, "bold"), fg="red", bg="#f0f0f0")
        self.title_label.pack(pady=10) 

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), padding=5)
        style.configure("TButton", font=("Arial", 10))

        frame = ttk.Frame(self.master, padding="10")
        frame.pack(expand=True)

        self.label_user = ttk.Label(frame, text="Tên đăng nhập:")
        self.label_user.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.entry_user = ttk.Entry(frame)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)

        self.label_pass = ttk.Label(frame, text="Mật khẩu:")
        self.label_pass.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        self.entry_pass = ttk.Entry(frame, show="*")
        self.entry_pass.grid(row=1, column=1, padx=10, pady=10)

        self.button_login = ttk.Button(frame, text="Đăng Nhập", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=20)

        # Tạo menu
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Tạo menu Help
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_warning)


    def show_warning(self):
        """Hàm hiển thị hộp thoại cảnh báo."""
        messagebox.showwarning("Python Message Warning Box",
                                "A Python GUI created using tkinter:\nWarning: There might be a bug in this code.")


        self.entry_user.focus()

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        # Hardcoded credentials for testing; modify as needed
        if username == "admin" and password == "password":
            self.master.destroy()
            main_app()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

class Sinhvien:
    def __init__(self, master):
        self.master = master
        self.master.title('Quản Lý Sinh Viên')
        self.master.geometry("600x700")
        self.master.configure(bg="#f0f0f0")

        self.title_label = tk.Label(self.master, text="QUẢN LÝ SINH VIÊN", font=("Times New Roman", 24, "bold"), fg="red", bg="#f0f0f0")
        self.title_label.pack(pady=20)

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), padding=5)
        style.configure("TButton", font=("Arial", 10))


        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(expand=True)
        

        # Entry for student information
        self.ten_sv = ttk.Label(main_frame, text='Nhập Họ và Tên:')
        self.ten_sv.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.ten_entry = ttk.Entry(main_frame)
        self.ten_entry.grid(row=0, column=1, padx=10, pady=10)

        self.mssv = ttk.Label(main_frame, text='Nhập MSSV:')
        self.mssv.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        self.mssv_entry = ttk.Entry(main_frame)
        self.mssv_entry.grid(row=1, column=1, padx=10, pady=10)

        self.gender_label = ttk.Label(main_frame, text='Chọn Giới tính:')
        self.gender_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.gender = tk.StringVar()
        self.gender.set("Nam")  # Default gender

        self.radio_male = ttk.Radiobutton(main_frame, text="Nam", variable=self.gender, value="Nam")
        self.radio_male.grid(row=2, column=1, padx=10, pady=5, sticky="W")

        self.radio_female = ttk.Radiobutton(main_frame, text="Nữ", variable=self.gender, value="Nữ")
        self.radio_female.grid(row=2, column=1, padx=10, pady=5, sticky="E")

        

        self.ten_entry.focus()

        

        # Create Treeview for student list
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Tên Sinh Viên", "Mã Số Sinh Viên", "Giới Tính"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên Sinh Viên", text="Họ và Tên")
        self.tree.heading("Mã Số Sinh Viên", text="MSSV")
        self.tree.heading("Giới Tính", text="Giới Tính")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Button Frame
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.grid(row=4, column=0, columnspan=2)

        action1 = ttk.Button(button_frame, text='Lưu thông tin', command=self.save_infor)
        action1.pack(side="left", padx=5, pady=10)

        action2 = ttk.Button(button_frame, text='Xóa Thông tin', command=self.delete_infor)
        action2.pack(side="left", padx=5, pady=10)

        # Search Frame
        search_frame = ttk.Frame(main_frame, padding="10")
        search_frame.grid(row=5, column=0, columnspan=2)

        self.search_label = ttk.Label(search_frame, text="Tìm kiếm sinh viên:")
        self.search_label.pack(side="left", padx=5)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        self.search_button = ttk.Button(search_frame, text="Tìm kiếm", command=self.search_infor)
        self.search_button.pack(side="left", padx=5)

        self.show_all_button = ttk.Button(search_frame, text="Hiển thị tất cả sinh viên", command=self.show_all_students)
        self.show_all_button.pack(side="left", padx=5)

        # Database connection
        self.conn = None
        self.cur = None
        self.connect_db()



    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="MydataBase",
                user="postgres",
                password="17468977",
                port="5432"
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Có lỗi xảy ra khi kết nối đến cơ sở dữ liệu: {e}")

            # Tạo menu
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Tạo menu Help
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_warning)


    def show_warning(self):
        """Hàm hiển thị hộp thoại cảnh báo."""
        messagebox.showwarning("Python Message Warning Box",
                                "A Python GUI created using tkinter:\nWarning: There might be a bug in this code.")

    def save_infor(self):
        ho_va_ten = self.ten_entry.get()
        ma_so_sv = self.mssv_entry.get()
        gender = self.gender.get()

        if ho_va_ten and ma_so_sv and gender:
            try:
                self.cur.execute(
                    'INSERT INTO "SinhVien" ("Tên Sinh Viên", "Mã Số Sinh Viên", "Giới Tính") VALUES (%s, %s, %s)', 
                    (ho_va_ten, ma_so_sv, gender))
                self.conn.commit()

                # Get the last inserted ID
                self.cur.execute('SELECT LASTVAL();')
                id_value = self.cur.fetchone()[0]

                # Insert into treeview
                self.tree.insert("", "end", values=(id_value, ho_va_ten, ma_so_sv, gender))
                messagebox.showinfo("Thành công", "Thông tin đã được lưu!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu thông tin: {e}")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!")

    def delete_infor(self):
        selected_item = self.tree.selection()

        if selected_item:
            item = self.tree.item(selected_item)
            id_value = item['values'][0]  # Get ID of the selected item

            try:
                self.cur.execute(
                    'DELETE FROM "SinhVien" WHERE "ID" = %s', 
                    (id_value,))
                self.conn.commit()

                # Remove from treeview
                self.tree.delete(selected_item)
                messagebox.showinfo("Thành công", "Thông tin đã được xóa!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi xóa thông tin: {e}")
        else:
            messagebox.showwarning("Lỗi", "Chưa chọn thông tin nào để xóa.")

    def search_infor(self):
        search_term = self.search_entry.get()
        if search_term:
            try:
                self.cur.execute(
                    'SELECT "ID", "Tên Sinh Viên", "Mã Số Sinh Viên", "Giới Tính" FROM "SinhVien" WHERE "Tên Sinh Viên" LIKE %s OR CAST("Mã Số Sinh Viên" AS TEXT) LIKE %s',  
                    (f'%{search_term}%', f'%{search_term}%'))
                results = self.cur.fetchall()

                self.tree.delete(*self.tree.get_children())
                for row in results:
                    self.tree.insert("", "end", values=row)
                if not results:
                    messagebox.showinfo("Kết quả", "Không tìm thấy sinh viên!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi tìm kiếm: {e}")
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập từ khóa tìm kiếm!")

    def show_all_students(self):
        try:
            self.cur.execute('SELECT "ID", "Tên Sinh Viên", "Mã Số Sinh Viên", "Giới Tính" FROM "SinhVien"')
            results = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in results:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi tải danh sách: {e}")

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

def main_app():
    win = tk.Tk()
    app = Sinhvien(win)
    win.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    login_app = Login(root)
    root.mainloop()