from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret"

# Cấu hình thư mục tải lên hình ảnh
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Dữ liệu tạm thời lưu các sản phẩm
products = []

@app.route("/")
def home():
    return render_template("add_product.html")

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        price = request.form['price']
        description = request.form['description']
        
        # Xử lý tải lên ảnh
        image_file = request.files['image']
        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        
        # Thêm sản phẩm vào danh sách với ID duy nhất
        product = {
            "id": len(products),  # Sử dụng độ dài danh sách làm ID
            "name": name,
            "code": code,
            "price": price,
            "description": description,
            "image_path": 'uploads/' + filename if image_path else 'uploads/default.jpg',
            "posted": False  # Đánh dấu sản phẩm chưa được đăng
        }
        products.append(product)

        flash("Sản phẩm đã được thêm thành công!")
        return redirect(url_for('product_list'))
    
    return render_template('add_product.html')

@app.route("/product_list")
def product_list():
    return render_template("product_list.html", products=products)

@app.route("/search_product", methods=["POST"])
def search_product():
    if request.method == "POST":
        query = request.form["query"].strip().lower()  # Lấy từ khóa tìm kiếm và chuyển thành chữ thường
        
        # Tìm sản phẩm theo mã sản phẩm
        results = [
            product for product in products 
            if query == product["code"].lower()  # Chỉ tìm khớp chính xác với mã sản phẩm
        ]
        
        if results:
            return render_template("product_list.html", products=results)
        else:
            flash("Không tìm thấy sản phẩm nào với mã sản phẩm đã nhập!")
            return redirect(url_for("product_list"))
    
    return redirect(url_for("product_list"))


@app.route("/edit_product/<int:product_id>", methods=["POST"])
def edit_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        product['name'] = request.form['name']
        product['code'] = request.form['code']
        product['price'] = request.form['price']
        product['description'] = request.form['description']
        
        # Cập nhật ảnh nếu có
        image_file = request.files.get('image')
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            product['image_path'] = 'uploads/' + filename

        flash("Sản phẩm đã được cập nhật!")
    else:
        flash("Không tìm thấy sản phẩm!")
    return redirect(url_for("product_list"))

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    flash("Sản phẩm đã được xóa!")
    return redirect(url_for("product_list"))

@app.route("/post_product/<int:product_id>")
def post_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        product["posted"] = True
        flash("Sản phẩm đã được đăng lên trang bán!")
    else:
        flash("Không tìm thấy sản phẩm!")
    return redirect(url_for("product_list"))

@app.route("/product_sales")
def product_sales():
    # Lọc các sản phẩm đã được đăng
    posted_products = [p for p in products if p.get("posted")]
    return render_template("product_sales.html", products=posted_products)

if __name__ == "__main__":
    app.run(debug=True)


    