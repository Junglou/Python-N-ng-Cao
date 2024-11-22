import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
from tkinter import Menu


class CalendarApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Ứng dụng xếp lịch làm việc')
        self.master.geometry("500x500")

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

        # Nút lưu sự kiện
        action2 = tk.Button(self.master, text='Lưu sự kiện!!', command=self.save_event)
        action2.pack(pady=10)

        # Nút xóa sự kiện
        action3 = tk.Button(self.master, text='Xóa sự kiện!!!', command=self.delete_event)
        action3.pack(pady=10)

    def show_warning(self):
        """Hàm hiển thị hộp thoại cảnh báo."""
        messagebox.showwarning(
            "Python Message Warning Box",
            "A Python GUI created using tkinter:\nWarning: There might be a bug in this code."
        )

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

            messagebox.showinfo("Thành công", "Sự kiện đã được lưu!")
        else:
            messagebox.showwarning("Cảnh Báo!!!!", "Vui Lòng nhập tên sự kiện")

    def delete_event(self):
        """Hàm xóa sự kiện."""
        select_index = self.list_event.curselection()
        if select_index:
            # Lấy sự kiện được chọn
            event = self.su_kien.pop(select_index[0])
            self.list_event.delete(select_index)

            messagebox.showinfo("Xóa sự kiện", f"Sự kiện '{event[0]}' vào ngày {event[1]} đã được xóa!")
        else:
            messagebox.showwarning("Không có sự kiện", "Không có sự kiện nào để xóa!!")


# Tạo cửa sổ chính
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
