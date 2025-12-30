# Data Mining Project - Online Retail Analysis

## 📁 Cấu trúc thư mục

```
DataMining/
│
├── data/
│   └── dataset.xlsx          # Dữ liệu gốc
│
├── notebooks/                # Jupyter notebooks
│
├── src/
│   ├── main.py              # File chạy chính
│   ├── processing/          # Các module xử lý
│   │   ├── __init__.py
│   │   └── data_ingestion.py
│   └── utils/
│
├── models/                   # Models đã train
│
├── mapped_data.csv          # Dữ liệu đã xử lý
├── item_mapping.json        # Mapping StockCode sang ID
├── requirements.txt
└── README.md
```

## 📦 Cài đặt

```bash
pip install -r requirements.txt
```

## 🚀 Sử dụng

### Chạy chương trình

```bash
py .\src\main.py
```

## 📊 Dataset: Online Retail

Dataset chứa thông tin giao dịch bán lẻ trực tuyến từ UK (2010-2011).

### Thành viên 1: Data Ingestion & Mapping (Xuân Minh)

**Nhiệm vụ:**
1. ✅ Load file Excel (Dùng pandas)
2. ✅ Tạo cột `Unit_Profit = UnitPrice × random.uniform(0.1, 0.4)`
3. ✅ Mã hóa `StockCode` thành ID số (1, 2, 3...)
4. ✅ Lưu mapping vào `item_mapping.json` (dictionary)
5. ✅ Output: `mapped_data.csv` (StockCode đã thay bằng ID số)

**Sử dụng module:**

```python
from processing import process_data

# Xử lý dữ liệu
df = process_data(
    input_file='src/data/dataset.xlsx',
    output_csv='mapped_data.csv',
    output_json='item_mapping.json'
)
```

## 📄 Output Files

- **mapped_data.csv**: Dataset với StockCode đã được mã hóa thành ID số
- **item_mapping.json**: Dictionary mapping `{"StockCode": ID_số}`
