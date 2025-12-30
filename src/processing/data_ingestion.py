import pandas as pd
import random
import json


def process_data(input_file, output_csv='mapped_data.csv', output_json='item_mapping.json', output_txt='transactions.txt'):
    """
    Xử lý dữ liệu từ file Excel:
    1. Đọc dữ liệu file excel
    2. Tạo cột Unit_Profit (10-40% UnitPrice)
    3. Mã hóa StockCode thành số nguyên
    4. Xuất file CSV, JSON mapping và TXT cho thuật toán
    
    Args:
        input_file: Đường dẫn đến file Excel
        output_csv: Tên file CSV output
        output_json: Tên file JSON mapping
        output_txt: Tên file TXT cho thuật toán (format: id:quantity:profit)
        
    Returns:
        DataFrame đã xử lý
    """
    # 1. Load file .xlsx
    print(f"Đang đọc dữ liệu từ {input_file}...")
    df = pd.read_excel(input_file)
    
    print(f"Shape của dataset: {df.shape}")
    print("\n5 dòng đầu tiên:")
    print(df.head())
    
    # 2. Tạo cột Unit_Profit (lợi nhuận từ 10-40% doanh thu)
    print("\nĐang tạo cột Unit_Profit...")
    df['Unit_Profit'] = df['UnitPrice'].apply(lambda price: price * random.uniform(0.1, 0.4))
    
    # 3. Mã hóa StockCode thành số nguyên
    print("\nĐang mã hóa StockCode...")
    stockcode_mapping = create_stockcode_mapping(df)
    
    # Lưu mapping vào file JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(stockcode_mapping, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu mapping của {len(stockcode_mapping)} StockCode vào {output_json}")
    
    # Thay thế StockCode bằng ID số
    df['StockCode'] = df['StockCode'].astype(str).map(stockcode_mapping)
    
    # 4. Lưu dữ liệu đã xử lý vào file CSV
    print(f"\nĐang lưu dữ liệu vào {output_csv}...")
    df.to_csv(output_csv, index=False, encoding='utf-8')
    
    # 5. Xuất file txt cho thuật toán (format: id:quantity:profit)
    print(f"\nĐang tạo file {output_txt} cho thuật toán...")
    with open(output_txt, 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            # Format: id:quantity:profit
            line = f"{int(row['StockCode'])}:{int(row['Quantity'])}:{row['Unit_Profit']:.2f}\n"
            f.write(line)
    print(f"Đã lưu {len(df)} giao dịch vào {output_txt}")
    
    print("\n=== Hoàn thành! ===")
    print(f"- File {output_csv}: {df.shape[0]} dòng, {df.shape[1]} cột")
    print(f"- File {output_json}: {len(stockcode_mapping)} mã sản phẩm")
    print(f"- File {output_txt}: {len(df)} giao dịch (format: id:quantity:profit)")
    print("\nMột số dòng dữ liệu sau khi xử lý:")
    print(df.head())
    
    return df


def create_stockcode_mapping(df):
    """
    Tạo dictionary mapping từ StockCode sang ID số nguyên
    
    Args:
        df: DataFrame chứa cột StockCode
        
    Returns:
        Dictionary mapping {stockcode: id}
    """
    unique_stockcodes = df['StockCode'].unique()
    stockcode_mapping = {str(code): idx + 1 for idx, code in enumerate(unique_stockcodes)}
    return stockcode_mapping
