from processing import process_data

if __name__ == "__main__":
    # Xử lý dữ liệu
    df = process_data(
        input_file='src/data/dataset.xlsx',
        output_csv='mapped_data.csv',
        output_json='item_mapping.json',
        output_txt='transactions.txt'
    )
