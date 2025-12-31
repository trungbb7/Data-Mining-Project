# 🛍️ Web Demo - Product Recommendation System

## Mô tả

Web demo đơn giản để hiển thị sản phẩm và gợi ý sản phẩm dựa trên luật kết hợp (Association Rules) từ Data Mining.

## Tính năng

### 1. Trang Danh Sách Sản Phẩm (index.html)
- ✅ Hiển thị tất cả sản phẩm từ file `products_with_price.csv`
- ✅ Tìm kiếm sản phẩm theo tên
- ✅ Lọc hiển thị sản phẩm unique (loại bỏ trùng lặp)
- ✅ Thêm sản phẩm vào giỏ hàng
- ✅ Hiển thị số lượng sản phẩm trong giỏ

### 2. Trang Giỏ Hàng (cart.html)
- ✅ Hiển thị danh sách sản phẩm trong giỏ
- ✅ Tính tổng tiền
- ✅ Xóa sản phẩm khỏi giỏ
- ✅ **Gợi ý sản phẩm thông minh** dựa trên:
  - Các sản phẩm đã có trong giỏ
  - Luật kết hợp từ file `recommendation_rules.json`
  - Expected utility (điểm ưu tiên)
- ✅ Thanh toán và xóa giỏ hàng

## Cấu trúc thư mục

```
web/
├── index.html          # Trang danh sách sản phẩm
├── cart.html          # Trang giỏ hàng
├── styles.css         # CSS styling
├── products.js        # Logic load data & quản lý giỏ hàng
├── app.js            # Logic trang sản phẩm
├── cart.js           # Logic trang giỏ hàng & recommendations
└── README.md         # File này
```

## Cách sử dụng

### Phương pháp 1: Mở trực tiếp bằng trình duyệt (Không hoạt động do CORS)

Do trình duyệt chặn CORS khi load file CSV/JSON từ local, bạn cần dùng local server.

### Phương pháp 2: Dùng Python HTTP Server (Khuyến nghị)

1. Mở terminal tại thư mục gốc của project (Data-Mining-Project)

2. Chạy lệnh:
```bash
# Python 3
python -m http.server 8000

# Hoặc Python 2
python -m SimpleHTTPServer 8000
```

3. Mở trình duyệt và truy cập:
```
http://localhost:8000/web/index.html
```

### Phương pháp 3: Dùng VS Code Live Server

1. Cài extension "Live Server" trong VS Code
2. Chuột phải vào file `index.html`
3. Chọn "Open with Live Server"

## Luồng hoạt động

1. **Người dùng vào trang sản phẩm**
   - Xem danh sách sản phẩm
   - Tìm kiếm sản phẩm
   - Thêm sản phẩm vào giỏ

2. **Người dùng vào trang giỏ hàng**
   - Xem sản phẩm đã chọn
   - Hệ thống tự động đề xuất sản phẩm dựa trên:
     - Luật: Nếu giỏ có sản phẩm A → gợi ý sản phẩm B
     - Sắp xếp theo expected_utility (cao → thấp)
   - Người dùng có thể thêm sản phẩm gợi ý vào giỏ
   - Thanh toán

## Dữ liệu sử dụng

### Input Files (từ thư mục `output/`)

1. **products_with_price.csv**
   - Danh sách tất cả sản phẩm với giá
   - Format: `Description,UnitPrice`

2. **recommendation_rules.json**
   - Luật kết hợp để gợi ý sản phẩm
   - Format:
   ```json
   {
     "input": ["Product A"],
     "suggest": "Product B",
     "expected_utility": 12345
   }
   ```

## Logic gợi ý sản phẩm

```javascript
// Khi người dùng có sản phẩm A, B trong giỏ
// Hệ thống tìm các rule có:
// - rule.input chứa A HOẶC B HOẶC [A, B]
// - rule.suggest KHÔNG có trong giỏ
// Sắp xếp theo expected_utility và hiển thị top 6
```

## Công nghệ sử dụng

- **HTML5** - Cấu trúc trang
- **CSS3** - Styling (gradient background, cards, responsive)
- **Vanilla JavaScript** - Logic (không dùng framework)
- **LocalStorage** - Lưu giỏ hàng
- **Fetch API** - Load CSV và JSON

## Giao diện

- ✨ Gradient background màu tím
- 📱 Responsive design
- 🎨 Material design inspired
- 🔍 Tìm kiếm real-time
- 💡 Hiển thị badge "GỢI Ý" cho sản phẩm được đề xuất
- ⭐ Hiển thị điểm utility cho mỗi gợi ý

## Lưu ý

- Giỏ hàng được lưu trong LocalStorage của trình duyệt
- Data được load từ file CSV và JSON (cần local server)
- Recommendation chỉ hoạt động khi có sản phẩm trong giỏ match với rules
- Hệ thống tự động loại bỏ sản phẩm đã có trong giỏ khỏi danh sách gợi ý

## Demo Screenshot

### Trang sản phẩm
- Grid layout hiển thị sản phẩm
- Thanh tìm kiếm
- Nút thêm vào giỏ

### Trang giỏ hàng
- Danh sách sản phẩm đã chọn
- Tổng tiền
- **Phần gợi ý sản phẩm** dựa trên Data Mining rules

---

**Tác giả**: Data Mining Team
**Ngày tạo**: 2026
