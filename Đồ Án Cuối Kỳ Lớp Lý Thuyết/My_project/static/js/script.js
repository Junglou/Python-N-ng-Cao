document.addEventListener("DOMContentLoaded", function() {
    // Xử lý nút "Đăng lên trang bán" cho mỗi sản phẩm
    const postButtons = document.querySelectorAll(".post-button");
    postButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            const productName = this.closest('li').querySelector('strong').innerText;
            alert(`${productName} đã được đăng thành công!`);
        });
    });

    // Xử lý nút chỉnh sửa sản phẩm
    const editButtons = document.querySelectorAll("button[onclick^='openEditForm']");
    editButtons.forEach(function(button) {
        button.addEventListener("click", function(event) {
            // Dừng sự kiện mặc định để tránh xung đột
            event.preventDefault();

            // Lấy productIndex từ thuộc tính onclick
            const productIndex = this.getAttribute('onclick').match(/\d+/)[0];

            // Mở form chỉnh sửa
            openEditForm(productIndex);
        });
    });
});

document.querySelector('.product-list').addEventListener('click', function(event) {
    if (event.target.classList.contains('post-button')) {
        const productName = event.target.closest('li').querySelector('strong').innerText;
        alert(`${productName} đã được đăng thành công!`);
    }
});

function openEditForm(productId) {
    // Tìm sản phẩm theo `id`
    const product = products.find(p => p.id === productId);

    if (!product) {
        alert('Không tìm thấy sản phẩm!');
        return;
    }

    // Điền dữ liệu sản phẩm vào form
    document.getElementById('name').value = product.name;
    document.getElementById('code').value = product.code;
    document.getElementById('price').value = product.price;
    document.getElementById('description').value = product.description;

    // Hiển thị form chỉnh sửa và overlay
    document.getElementById('editForm').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';

    // Cập nhật action của form với product_id
    document.querySelector('#editForm form').action = "{{ url_for('edit_product', product_id='') }}".replace('', productId);
}


