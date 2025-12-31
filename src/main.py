from processing import process_data

if __name__ == "__main__":
    # Xử lý dữ liệu
    df = process_data(
        input_file='src/data/dataset.xlsx',
        output_csv='data/processed/mapped_data.csv',
        output_json='data/processed/item_mapping.json'
    )
