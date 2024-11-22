from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import psycopg2

app = Flask(__name__)
app.secret_key = "secret"

# Cấu hình cơ sở dữ liệu PostgreSQL
DB_HOST = "localhost"
DB_NAME = "MydataBase"
DB_USER = "postgres"
DB_PASSWORD = "17468977"

# Hàm kết nối đến cơ sở dữ liệu
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Cấu hình thư mục tải lên hình ảnh
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Trang chủ
@app.route("/")
def home():
    return render_template("add_product.html")

# Thêm sản phẩm
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        price = request.form['price']
        description = request.form['description']
        image_file = request.files['image']

        # Xử lý ảnh tải lên
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        # Lưu thông tin sản phẩm vào cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, code, price, description, image_path)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, code, price, description, f'uploads/{filename}'))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Sản phẩm đã được thêm thành công!")
        return redirect(url_for('product_list'))

    return render_template('add_product.html')

# Danh sách sản phẩm
@app.route("/product_list")
def product_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, code, price, description, image_path, posted FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Chuyển đổi tuple thành danh sách dictionary
    products = [
        {
            "id": row[0],
            "name": row[1],
            "code": row[2],
            "price": row[3],
            "description": row[4],
            "image_path": row[5],
            "posted": row[6]
        }
        for row in rows
    ]
    return render_template("product_list.html", products=products)

# Tìm kiếm sản phẩm
@app.route("/search_product", methods=["POST"])
def search_product():
    query = request.form["query"].strip().lower()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, code, price, description, image_path, posted FROM products WHERE LOWER(code) = %s", (query,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    products = [
        {
            "id": row[0],
            "name": row[1],
            "code": row[2],
            "price": row[3],
            "description": row[4],
            "image_path": row[5],
            "posted": row[6]
        }
        for row in rows
    ]

    if products:
        return render_template("product_list.html", products=products)
    else:
        flash("Không tìm thấy sản phẩm nào với mã sản phẩm đã nhập!")
        return redirect(url_for("product_list"))

# Chỉnh sửa sản phẩm
@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form['name']
        code = request.form['code']
        price = request.form['price']
        description = request.form['description']

        # Xử lý ảnh nếu được tải lên
        image_file = request.files.get('image')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            cursor.execute("""
                UPDATE products SET name = %s, code = %s, price = %s, description = %s, image_path = %s
                WHERE id = %s
            """, (name, code, price, description, f'uploads/{filename}', product_id))
        else:
            cursor.execute("""
                UPDATE products SET name = %s, code = %s, price = %s, description = %s
                WHERE id = %s
            """, (name, code, price, description, product_id))

        conn.commit()
        cursor.close()
        conn.close()
        flash("Sản phẩm đã được cập nhật!")
        return redirect(url_for("product_list"))

    # Lấy thông tin sản phẩm để hiển thị
    cursor.execute("SELECT id, name, code, price, description, image_path FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()

    if product:
        product = {
            "id": product[0],
            "name": product[1],
            "code": product[2],
            "price": product[3],
            "description": product[4],
            "image_path": product[5]
        }
        return render_template("edit_product.html", product=product)
    else:
        flash("Không tìm thấy sản phẩm!")
        return redirect(url_for("product_list"))

# Xóa sản phẩm
@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
     # Xóa tất cả sản phẩm và đặt lại ID
    cursor.execute("TRUNCATE TABLE products RESTART IDENTITY CASCADE;")
    conn.commit()
    cursor.close()
    conn.close()
    flash("Sản phẩm đã được xóa!")
    return redirect(url_for("product_list"))

# Đăng sản phẩm
@app.route("/post_product/<int:product_id>")
def post_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET posted = TRUE WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Sản phẩm đã được đăng!")
    return redirect(url_for("product_list"))

# Danh sách sản phẩm đã đăng
@app.route("/product_sales")
def product_sales():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, code, price, description, image_path FROM products WHERE posted = TRUE")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    products = [
        {
            "id": row[0],
            "name": row[1],
            "code": row[2],
            "price": row[3],
            "description": row[4],
            "image_path": row[5]
        }
        for row in rows
    ]
    return render_template("product_sales.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
