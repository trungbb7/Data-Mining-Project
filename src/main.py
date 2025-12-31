from processing.data_ingestion import process_data
from processing.data_cleaning import clean_and_filter_data

if __name__ == "__main__":
    # Xử lý dữ liệu -- Member 1
    df = process_data(
        input_file='src/data/dataset.xlsx',
        output_csv='data/processed/mapped_data.csv',
        output_json='data/processed/item_mapping.json'
    )
    
    # Cleaning & Filtering -- Member 3
    df_clean = clean_and_filter_data(
        input_file='data/processed/mapped_data.csv',
        mapping_file='data/processed/item_mapping.json',
        output_file='data/processed/clean_transactions_spmf.txt'
    )
