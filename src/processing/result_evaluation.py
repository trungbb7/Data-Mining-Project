import json
import pandas as pd
from itertools import combinations

# 1. LOAD DỮ LIỆU
# Load mapping (Output của TV1)
with open("item_mapping.json", "r") as f:
    id_to_name = json.load(f)  # Dạng {'1': 'Ao thun', '2': 'Quan jean'}


# Load kết quả mining (Output của TV4)
def parse_spmf_output(filepath):
    results = []
    with open(filepath, "r") as f:
        for line in f:
            # Format giả định: 1 5 12 #UTIL: 5000
            parts = line.strip().split("#UTIL:")
            items_str = parts[0].strip().split(" ")
            utility = int(parts[1])

            # Chuyển ID sang Tên
            item_names = [id_to_name.get(i, f"Unknown_{i}") for i in items_str]
            results.append({"items": item_names, "utility": utility})
    return pd.DataFrame(results)


df_hui = parse_spmf_output("high_utility_itemsets.txt")

# 2. PHÂN TÍCH (Lọc Top lợi nhuận cao nhất)
top_hui = df_hui.sort_values(by="utility", ascending=False).head(20)
print("Top 20 bộ sản phẩm lãi cao nhất:\n", top_hui)

# 3. TẠO LUẬT GỢI Ý (CHO TV6)
# Logic: Với tập {A, B, C}, nếu user mua {A, B} -> Gợi ý C
rules = []

for index, row in df_hui.iterrows():
    items = row["items"]
    util = row["utility"]

    # Chỉ xét các tập có từ 2 sản phẩm trở lên
    if len(items) >= 2:
        # Tạo luật: Bỏ 1 phần tử ra làm phần tử gợi ý
        for i in range(len(items)):
            target = items[i]  # Món sẽ gợi ý
            antecedent = items[:i] + items[i + 1 :]  # Những món khách đã chọn

            # Lưu luật
            rule = {
                "input": sorted(antecedent),  # Sort để dễ so khớp
                "suggest": target,
                "expected_utility": util,
            }
            rules.append(rule)

# Xuất file JSON cho Web App
with open("final_rules_for_app.json", "w") as f:
    json.dump(rules, f, indent=4)

print(f"Đã tạo {len(rules)} luật gợi ý cho Web App.")
