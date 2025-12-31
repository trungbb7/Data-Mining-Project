import pandas as pd
import json


def clean_and_filter_data(
    input_file="../../data/processed/mapped_data.csv",
    mapping_file="../../data/processed/item_mapping.json",
    output_file="../../data/processed/clean_transactions_spmf.txt",
):
    """
    Cleaning & Filtering (Xử lý nhiễu đặc thù)
    Nhiệm vụ: "Dọn rác" đặc trưng của bộ Online Retail

    Các bước:
    1. Lọc đơn hủy: Loại bỏ dòng có Invoice bắt đầu bằng chữ 'C'
    2. Lọc mã hàng rác: Loại bỏ các StockCode đặc biệt (POST, M, BANK CHARGES, D)
    3. Xử lý giá trị âm: Loại bỏ dòng có Price <= 0 hoặc Quantity <= 0
    4. Convert dữ liệu sang format SPMF (itemid:quantity:unit_profit)

    Args:
        input_file: Đường dẫn file CSV đã được xử lý (có StockCode, Unit_Profit)
        mapping_file: File JSON chứa mapping StockCode -> ID
        output_file: File output SPMF format

    Returns:
        DataFrame đã clean
    """
    # Load dữ liệu từ mapped_data.csv (đã có Unit_Profit và StockCode là ID)
    df = pd.read_csv(input_file)
    original_count = len(df)

    # Load item_mapping.json để lọc mã rác
    with open(mapping_file, "r", encoding="utf-8") as f:
        stockcode_mapping = json.load(f)

    # Tìm ID của các mã đặc biệt cần lọc
    special_codes = ["POST", "M", "BANK CHARGES", "D"]
    special_ids = [
        stockcode_mapping.get(code)
        for code in special_codes
        if code in stockcode_mapping
    ]

    # Lọc đơn hủy (Invoice bắt đầu bằng 'C')
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df = df[~df["InvoiceNo"].str.startswith("C")]

    # Lọc mã hàng rác (sử dụng ID từ mapping)
    if special_ids:
        df = df[~df["StockCode"].isin(special_ids)]

    # Xử lý giá trị âm (Price <= 0 hoặc Quantity <= 0)
    df = df[(df["UnitPrice"] > 0) & (df["Quantity"] > 0)]

    # Convert sang format SPMF (gom theo InvoiceNo)
    # Mỗi dòng = 1 transaction, các items cách nhau bởi khoảng trắng
    # Format: itemid:quantity:unit_profit itemid:quantity:unit_profit ...
    transactions_written = 0
    with open(output_file, "w", encoding="utf-8") as f:
        for invoice_no, group in df.groupby("InvoiceNo"):
            items = []
            for _, row in group.iterrows():
                item_str = f"{int(row['StockCode'])}:{int(row['Quantity'])}:{row['Unit_Profit']:.2f}"
                items.append(item_str)

            if items:
                f.write(" ".join(items) + "\n")
                transactions_written += 1

    print(
        f"Cleaned: {original_count:,} → {len(df):,} items → {transactions_written:,} transactions → {output_file}"
    )

    return df


def preview_spmf_file(
    file_path="data/processed/clean_transactions_spmf.txt", num_lines=10
):
    """Xem trước nội dung file SPMF"""
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= num_lines:
                break
            print(f"{i+1:3d}: {line.strip()}")


df = clean_and_filter_data()
df.to_csv("../data/cleaned_dataset.csv")
