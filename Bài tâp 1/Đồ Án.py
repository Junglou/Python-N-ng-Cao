import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import psycopg2
from datetime import datetime  # Thêm thư viện datetime
from tkinter import Menu

class CalendarApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Ứng dụng xếp lịch làm việc')
        self.master.geometry("400x400")

        # Tạo menu
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Tạo menu File
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

        # Tạo lịch
        self.cal = Calendar(self.master, selectmode='day')
        self.cal.pack(pady=20)

        # Nhập tên sự kiện
        self.label_event = tk.Label(self.master, text="Vui lòng nhập tên sự kiện!!!")
        self.label_event.pack(pady=10)
        self.name_event = tk.Entry(self.master)
        self.name_event.pack(pady=10)

        # Danh sách sự kiện
        self.label_list = tk.Label(self.master, text="Chọn sự kiện để xóa!!")
        self.label_list.pack(pady=10)
        self.list_event = tk.Listbox(self.master, height=8, width=50)
        self.list_event.pack(pady=10)

        # Danh sách sự kiện
        self.su_kien = []

    def ket_noi_database(self):
        """Hàm để kết nối với cơ sở dữ liệu."""
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="MydataBase",
                user="postgres",
                password="17468977",
                port="5432"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối với cơ sở dữ liệu: {str(e)}")
            return None

    def Nhap_database(self, event_name, event_date):
        """Hàm nhập dữ liệu vào cơ sở dữ liệu."""
        conn = self.ket_noi_database()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    'INSERT INTO "AppCalendar" ("Tên Sự Kiện", "Ngày Diễn Ra") VALUES (%s, %s)',
                    (event_name, event_date)
                )
                conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
                messagebox.showinfo("Thành công", "Sự kiện đã được lưu vào cơ sở dữ liệu!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi lưu sự kiện: {str(e)}")
            finally:
                cur.close()
                conn.close()

    def save_event(self):
        """Hàm lưu sự kiện."""
        ten_sukien = self.name_event.get()
        select_day = self.cal.get_date()

        try:
            # Chuyển đổi định dạng ngày thành YYYY-MM-DD
            formatted_date = datetime.strptime(select_day, '%m/%d/%y').strftime('%Y-%m-%d')
        except ValueError as e:
            messagebox.showerror("Lỗi định dạng ngày", f"Định dạng ngày không hợp lệ: {str(e)}")
            return

        if ten_sukien:
            # Lưu vào giao diện
            event = f"{ten_sukien} | Ngày: {formatted_date}"
            self.su_kien.append((ten_sukien, formatted_date))  # Lưu tuple vào danh sách
            self.list_event.insert(tk.END, event)

            # Lưu vào cơ sở dữ liệu
            self.Nhap_database(ten_sukien, formatted_date)
        else:
            messagebox.showwarning("Cảnh Báo!!!!", "Vui Lòng nhập tên sự kiện")
    
        # Nút lưu sự kiện
        action2 = tk.Button(self.master, text='Lưu sự kiện!!', command=self.save_event)
        action2.pack(pady=10)

    def Xoa_database(self, event_name, event_date):
        """Hàm xóa sự kiện khỏi cơ sở dữ liệu."""
        conn = self.ket_noi_database()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    'DELETE FROM "AppCalendar" WHERE "Tên Sự Kiện" = %s AND "Ngày Diễn Ra" = %s',
                    (event_name, event_date)
                )
                conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xóa sự kiện: {str(e)}")
            finally:
                cur.close()
                conn.close()

    def delete_event(self):
        """Hàm xóa sự kiện."""
        select_index = self.list_event.curselection()
        if select_index:
            # Lấy sự kiện được chọn
            event = self.su_kien.pop(select_index[0])
            self.list_event.delete(select_index)

            # Xóa sự kiện khỏi cơ sở dữ liệu
            self.Xoa_database(event[0], event[1])  # event[0] là tên sự kiện, event[1] là ngày

            messagebox.showinfo("Xóa sự kiện", f"Sự kiện '{event[0]}' vào ngày {event[1]} đã được xóa!")
        else:
            messagebox.showwarning("Không có sự kiện", "Không có sự kiện nào để xóa!!")

    # Nút xóa sự kiện
        action3 = tk.Button(self.master, text='Xóa sự kiện!!!', command=self.delete_event)
        action3.pack(pady=10)


# Tạo cửa sổ chính
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
