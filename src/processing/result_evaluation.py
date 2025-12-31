import pandas as pd
import json

# LOAD DỮ LIỆU
cleaned_df = pd.read_csv("../data/cleaned_dataset.csv")
code_name_df = cleaned_df[["StockCode", "Description"]].drop_duplicates()
code_to_name = code_name_df.set_index("StockCode")["Description"].to_dict()


# Load kết quả mining
def parse_spmf_output(filepath):
    results = []
    with open(filepath, "r") as f:
        for line in f:
            if not "#UTIL:" in line:
                continue

            # Format giả định: 1 5 12 #UTIL: 5000
            parts = line.strip().split("#UTIL:")
            items_str = parts[0].strip().split(" ")
            utility = round(float(parts[1].strip().split(" #SUP: ")[0]))

            # Chuyển ID sang Tên
            item_names = [code_to_name.get(int(i), f"Unknown_{i}") for i in items_str]
            results.append({"items": item_names, "utility": utility})
    return pd.DataFrame(results)


def generate_rules(filepath, rules_output, products_with_price_output):

    df_hui = parse_spmf_output(filepath)
    # TẠO LUẬT
    # Logic: Với tập {A, B, C}, nếu user mua {A, B} -> Gợi ý C
    rules = []
    product_names = set()
    for index, row in df_hui.iterrows():
        items = row["items"]
        util = row["utility"]

        # Chỉ xét các tập có từ 2 sản phẩm trở lên
        if len(items) >= 2:
            # Tạo luật: Bỏ 1 phần tử ra làm phần tử gợi ý
            for i in range(len(items)):
                target = items[i]  # Món sẽ gợi ý
                antecedent = items[:i] + items[i + 1 :]  # Những món khách đã chọn

                product_names.add(target)

                # Lưu luật
                rule = {
                    "input": sorted(antecedent),  # Sort để dễ so khớp
                    "suggest": target,
                    "expected_utility": util,
                }
                rules.append(rule)

    # Xuất danh sách sản phẩm kèm giá
    products_with_price = cleaned_df[
        cleaned_df["Description"].isin(product_names)
    ].drop_duplicates()[["Description", "UnitPrice"]]
    products_with_price.to_csv(products_with_price_output, index=None)

    print(len(product_names))
    # Xuất file JSON cho Web App
    with open(rules_output, "w") as f:
        json.dump(rules, f, indent=4)

    print(f"Đã tạo {len(rules)} luật.")


generate_rules(
    filepath="../../output/patterns/high_utility_itemsets_10000.txt",
    rules_output="../../output/recommendation_rules.json",
    products_with_price_output="../../output/products_with_price.csv",
)
