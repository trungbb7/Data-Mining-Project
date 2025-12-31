import json
from collections import defaultdict
from itertools import combinations
import os
import time

def load_item_mapping(mapping_file='data/processed/item_mapping.json'):
    with open(mapping_file, 'r', encoding='utf-8') as f:
        stockcode_mapping = json.load(f)
    id_to_stockcode = {v: k for k, v in stockcode_mapping.items()}
    return id_to_stockcode

def parse_spmf_file(input_file):
    transactions = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            transaction = {}
            # Tính transaction utility (TU) để dùng cho pruning sau này
            tu = 0
            items = line.split()
            for item in items:
                parts = item.split(':')
                if len(parts) == 3:
                    item_id = int(parts[0])
                    quantity = int(parts[1])
                    profit = float(parts[2])
                    transaction[item_id] = (quantity, profit)
                    tu += quantity * profit
            
            if transaction:
                transactions.append({'items': transaction, 'tu': tu})
    return transactions

def calculate_utility(itemset, transaction_items):
    utility = 0
    for item_id in itemset:
        if item_id in transaction_items:
            quantity, profit = transaction_items[item_id]
            utility += quantity * profit
    return utility

def find_high_utility_itemsets_optimized(transactions, min_utility, max_size=3):
    high_utility_itemsets = {}
    
    # --- PHASE 1: SIZE 1 ---
    print(f"  • [Pharse 1] Checking Size 1...")
    # Tính TWU cho từng item (Transaction-Weighted Utility)
    # TWU(item) = sum(TU of transactions containing item)
    twu = defaultdict(float)
    item_utility = defaultdict(float)
    item_support = defaultdict(int)
    
    for t in transactions:
        tu = t['tu']
        t_items = t['items']
        for item_id, (qty, profit) in t_items.items():
            twu[item_id] += tu
            item_utility[item_id] += (qty * profit)
            item_support[item_id] += 1
            
    # Lọc các item có TWU >= min_utility (Pruning property: nếu TWU < min_util thì itemset chứa nó cũng < min_util)
    promising_items = [item for item, val in twu.items() if val >= min_utility]
    promising_items.sort() # Sắp xếp để duyệt hiệu quả
    
    print(f"    - Found {len(promising_items)} promising items (TWU >= {min_utility}) out of {len(twu)} total.")
    
    # Lưu kết quả size 1
    count_size1 = 0
    for item in promising_items:
        if item_utility[item] >= min_utility:
            high_utility_itemsets[(item,)] = {
                'utility': item_utility[item],
                'support': item_support[item]
            }
            count_size1 += 1
    print(f"    - Found {count_size1} High-Utility Itemsets (Size 1)")

    if max_size == 1:
        return high_utility_itemsets

    # --- PHASE 2: SIZE 2 (Optimized) ---
    print(f"  • [Phase 2] Checking Size 2 (Pruned Search)...")
    count_size2 = 0
    
    # Chỉ xét các cặp item (a, b) mà cả a và b đều là promising items
    # Để tối ưu hơn: chỉ xét các cặp (a, b) cùng xuất hiện trong transaction nào đó
    
    # Xây dựng index ngược: item -> list of transaction indices
    item_to_tids = defaultdict(list)
    for idx, t in enumerate(transactions):
        for item in t['items']:
            if item in promising_items: # Chỉ index các item tiềm năng
                item_to_tids[item].append(idx)
    
    # Duyệt đôi một các promising items
    # Cách tối ưu: duyệt a, sau đó duyệt b > a
    processed_pairs = 0
    total_pairs_estimate = len(promising_items) * (len(promising_items)-1) / 2
    
    for i in range(len(promising_items)):
        item_a = promising_items[i]
        tids_a = set(item_to_tids[item_a])
        
        # Chỉ check b > item_a
        for j in range(i + 1, len(promising_items)):
            item_b = promising_items[j]
            
            # Intersection của transaction IDs: tìm các đơn hàng có cả A và B
            # (Thực tế intersection list đã sort sẽ nhanh hơn set, nhưng set code ngắn gọn cho demo)
            common_tids = tids_a.intersection(item_to_tids[item_b])
            
            if not common_tids:
                continue
                
            # Tính Upper Bound Utility cho cặp (A, B) trên các transaction chung
            # UB = Sum(TU of common transactions)
            ub_utility = 0
            for tid in common_tids:
                ub_utility += transactions[tid]['tu']
            
            # Pruning
            if ub_utility < min_utility:
                continue
            
            # Nếu qua được pruning, tính utility thật
            real_utility = 0
            for tid in common_tids:
                t = transactions[tid]['items']
                # Utility của cặp = util(A) + util(B) trong trans đó
                u_a = t[item_a][0] * t[item_a][1]
                u_b = t[item_b][0] * t[item_b][1]
                real_utility += (u_a + u_b)
            
            if real_utility >= min_utility:
                high_utility_itemsets[(item_a, item_b)] = {
                    'utility': real_utility,
                    'support': len(common_tids)
                }
                count_size2 += 1
                
        if i % 100 == 0:
            print(f"\r    - Processed {i}/{len(promising_items)} primary items...", end="")
            
    print(f"\n    - Found {count_size2} High-Utility Itemsets (Size 2)")
    
    return high_utility_itemsets

def save_results(itemsets, output_file, id_to_stockcode):
    sorted_itemsets = sorted(itemsets.items(), key=lambda x: x[1]['utility'], reverse=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# High-Utility Itemsets\n# Total: {len(sorted_itemsets)}\n\n")
        for itemset, info in sorted_itemsets:
            items_str = ' '.join(str(item) for item in itemset)
            f.write(f"{items_str} #UTIL: {info['utility']:.2f} #SUP: {info['support']}\n")
            
    readable_file = output_file.replace('.txt', '_readable.txt')
    with open(readable_file, 'w', encoding='utf-8') as f:
        f.write(f"# High-Utility Itemsets (Readable)\n# Total: {len(sorted_itemsets)}\n\n")
        for itemset, info in sorted_itemsets:
            stockcodes = [id_to_stockcode.get(item, f"ID{item}") for item in itemset]
            f.write(f"{' '.join(stockcodes)} #UTIL: {info['utility']:.2f} #SUP: {info['support']}\n")
    
    return len(sorted_itemsets)

def run_experiments():
    print("\n" + "="*60)
    print("  MINING: FAST OPTIMIZED VERSION (Max Size 2)")
    print("="*60)
    
    id_to_stockcode = load_item_mapping()
    print(f"✓ Loaded mapping ({len(id_to_stockcode)} items)")
    
    transactions = parse_spmf_file('data/processed/clean_transactions_spmf.txt')
    print(f"✓ Loaded data ({len(transactions)} transactions)")
    
    # Chạy thử nghiệm
    thresholds = [
        (1000, "Ngưỡng thấp"),
        (5000, "Ngưỡng trung bình"),
        (10000, "Ngưỡng cao")
    ]
    
    results = []
    
    for min_util, desc in thresholds:
        print(f"\n>>> Running Min Utility: £{min_util:,} ({desc})")
        start_time = time.time()
        
        # Max size = 2 để đảm bảo tốc độ
        itemsets = find_high_utility_itemsets_optimized(transactions, min_util, max_size=2)
        
        duration = time.time() - start_time
        print(f"    Done in {duration:.2f}s")
        
        # Lưu vào folder patterns
        output_file = f'output/patterns/high_utility_itemsets_{min_util}.txt'
        num = save_results(itemsets, output_file, id_to_stockcode)
        
        results.append({'threshold': min_util, 'num': num, 'file': output_file})

    # Summary report
    with open('output/mining_results_summary.txt', 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO KẾT QUẢ MINING (OPTIMIZED)\n==================================\n\n")
        for r in results:
            # Fix path display for summary
            new_path = r['file'].replace('output/', 'output/patterns/')
            f.write(f"Min Utility £{r['threshold']:,}: {r['num']} patterns -> {new_path}\n")
            
    print("\n✓ ALL DONE! Summary saved.")

if __name__ == "__main__":
    run_experiments()
