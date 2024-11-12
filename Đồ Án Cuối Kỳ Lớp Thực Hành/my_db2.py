import psycopg2
from tkinter import messagebox

class D_T_B2:
    def __init__(self):
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

    def save_infor(self, ho_va_ten, ma_so_sv, gender, email, dia_chi):
        try:
            self.cur.execute(
                'INSERT INTO "SinhVien" ("Tên Sinh Viên", "Mã Số Sinh Viên", "Giới Tính", "Email", "Địa Chỉ") VALUES (%s, %s, %s, %s, %s)',
                (ho_va_ten, ma_so_sv, gender, email, dia_chi))
            self.conn.commit()
            self.cur.execute('SELECT LASTVAL();')
            return self.cur.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu thông tin: {e}")
            return None

    def delete_infor(self, id_value):
        try:
            self.cur.execute('DELETE FROM "SinhVien" WHERE "ID" = %s', (id_value,))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi xóa thông tin: {e}")

    def search_infor(self, search_term):
        try:
            self.cur.execute(
                'SELECT "ID", "Tên Sinh Viên", "Mã Số Sinh Viên", "Giới Tính", "Email", "Địa Chỉ" FROM "SinhVien" '
                'WHERE "Tên Sinh Viên" LIKE %s OR CAST("Mã Số Sinh Viên" AS TEXT) LIKE %s OR "Email" LIKE %s OR "Địa Chỉ" LIKE %s',
                (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            return self.cur.fetchall()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi tìm kiếm: {e}")
            return []

    def show_all_students(self):
        try:
            self.cur.execute('SELECT "ID", "Tên Sinh Viên", "Mã Số Sinh Viên", "Giới Tính", "Email", "Địa Chỉ" FROM "SinhVien"')
            return self.cur.fetchall()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi tải danh sách: {e}")
            return []

    def close(self):
        if self.cur:
            try:
                self.cur.execute('TRUNCATE TABLE "SinhVien" RESTART IDENTITY')
                self.conn.commit()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi xóa dữ liệu: {e}")

            self.cur.close()
        
        if self.conn:
            self.conn.close()
