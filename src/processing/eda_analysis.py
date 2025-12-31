import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Cấu hình matplotlib để hiển thị tiếng Việt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Thiết lập style
sns.set_style("whitegrid")
sns.set_palette("husl")


def load_data(file_path='src/data/dataset.xlsx'):
    """Load dữ liệu từ file Excel"""
    print(f"Đang load dữ liệu từ {file_path}...")
    df = pd.read_excel(file_path)
    print(f" Đã load {len(df):,} dòng dữ liệu")
    return df


def analyze_country_distribution(df):
    """
    Phân tích 1: Phân bố theo Country
    Trả về: DataFrame thống kê và đề xuất lọc
    """
    print("1. PHÂN TÍCH PHÂN BỐ COUNTRY")
    
    # Thống kê theo country
    country_stats = df.groupby('Country').agg({
        'InvoiceNo': 'count',
        'Quantity': 'sum',
        'UnitPrice': lambda x: (x * df.loc[x.index, 'Quantity']).sum()  # Total Revenue
    }).rename(columns={
        'InvoiceNo': 'Transactions',
        'Quantity': 'Total_Quantity',
        'UnitPrice': 'Total_Revenue'
    })
    
    # Tính phần trăm
    country_stats['Trans_Percent'] = (country_stats['Transactions'] / country_stats['Transactions'].sum() * 100)
    country_stats = country_stats.sort_values('Transactions', ascending=False)
    
    # Hiển thị top 10
    print("\nTop 10 quốc gia theo số lượng giao dịch:")
    print(country_stats.head(10).to_string())
    
    # Thống kê UK
    uk_percent = country_stats.loc['United Kingdom', 'Trans_Percent']
    uk_transactions = country_stats.loc['United Kingdom', 'Transactions']
    total_transactions = country_stats['Transactions'].sum()
    
    print(f"\n Thống kê UK:")
    print(f"   - Số giao dịch: {uk_transactions:,} / {total_transactions:,}")
    print(f"   - Chiếm: {uk_percent:.2f}% tổng giao dịch")
    print(f"   - Số quốc gia khác: {len(country_stats) - 1}")
    
    # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    top_countries = country_stats.head(15)
    colors = ['#FF6B6B' if country == 'United Kingdom' else '#4ECDC4' for country in top_countries.index]
    
    plt.barh(range(len(top_countries)), top_countries['Transactions'], color=colors)
    plt.yticks(range(len(top_countries)), top_countries.index)
    plt.xlabel('Số lượng giao dịch', fontsize=12)
    plt.title('Top 15 quốc gia theo số lượng giao dịch', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Thêm nhãn giá trị
    for i, (country, row) in enumerate(top_countries.iterrows()):
        plt.text(row['Transactions'], i, f"  {row['Trans_Percent']:.1f}%", 
                va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('output/eda_country_distribution.png', dpi=300, bbox_inches='tight')
    print("\n Đã lưu biểu đồ: output/eda_country_distribution.png")
    plt.close()
    
    # Đề xuất
    print("\n ĐỀ XUẤT:")
    if uk_percent > 80:
        print(f"   → NÊN LỌC CHỈ GIỮ 'United Kingdom' vì:")
        print(f"     • Chiếm {uk_percent:.1f}% dữ liệu (áp đảo)")
        print(f"     • Dữ liệu đồng nhất về thị trường và hành vi khách hàng")
        print(f"     • Giảm nhiễu từ các thị trường nhỏ")
    else:
        print(f"   → CÂN NHẮC GIỮ NHIỀU QUỐC GIA vì UK chỉ chiếm {uk_percent:.1f}%")
    
    return country_stats


def analyze_quantity_outliers(df):
    """
    Phân tích 2: Tìm outliers trong Quantity
    """
    print("2. PHÂN TÍCH QUANTITY & OUTLIERS")
    
    # Lọc Quantity > 0 (bỏ đơn hủy/trả hàng)
    df_positive = df[df['Quantity'] > 0].copy()
    
    # Thống kê mô tả
    print("\nThống kê Quantity (chỉ đơn hàng dương):")
    print(df_positive['Quantity'].describe())
    
    # Tính quartiles và IQR
    Q1 = df_positive['Quantity'].quantile(0.25)
    Q3 = df_positive['Quantity'].quantile(0.75)
    IQR = Q3 - Q1
    outlier_threshold = Q3 + 1.5 * IQR
    
    print(f"\n Phân tích Outliers:")
    print(f"   - Q1 (25%): {Q1:.0f}")
    print(f"   - Q3 (75%): {Q3:.0f}")
    print(f"   - IQR: {IQR:.0f}")
    print(f"   - Ngưỡng outlier (Q3 + 1.5*IQR): {outlier_threshold:.0f}")
    
    # Tìm outliers
    outliers = df_positive[df_positive['Quantity'] > outlier_threshold]
    print(f"   - Số đơn hàng outlier: {len(outliers):,} / {len(df_positive):,} ({len(outliers)/len(df_positive)*100:.2f}%)")
    print(f"   - Quantity lớn nhất: {df_positive['Quantity'].max():,}")
    
    # Top 10 đơn hàng có Quantity cao nhất
    print("\nTop 10 đơn hàng có Quantity cao nhất:")
    top_qty = df_positive.nlargest(10, 'Quantity')[['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'UnitPrice', 'Country']]
    print(top_qty.to_string(index=False))
    
    # Vẽ biểu đồ phân phối
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(df_positive['Quantity'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0].axvline(outlier_threshold, color='red', linestyle='--', linewidth=2, label=f'Ngưỡng outlier: {outlier_threshold:.0f}')
    axes[0].set_xlabel('Quantity', fontsize=11)
    axes[0].set_ylabel('Số lượng đơn hàng', fontsize=11)
    axes[0].set_title('Phân phối Quantity', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].set_xlim(0, min(outlier_threshold * 2, df_positive['Quantity'].max()))
    
    # Box plot
    axes[1].boxplot(df_positive['Quantity'], vert=True)
    axes[1].set_ylabel('Quantity', fontsize=11)
    axes[1].set_title('Box Plot - Quantity', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/eda_quantity_outliers.png', dpi=300, bbox_inches='tight')
    print("\n✓ Đã lưu biểu đồ: output/eda_quantity_outliers.png")
    plt.close()
    
    # Đề xuất
    print("\n ĐỀ XUẤT:")
    outlier_percent = len(outliers) / len(df_positive) * 100
    if outlier_percent > 5:
        print(f"   → CÓ THỂ LỌC BỎ outliers (>{outlier_threshold:.0f}) vì:")
        print(f"     • Chiếm {outlier_percent:.2f}% dữ liệu")
        print(f"     • Có thể là đơn bán buôn, không đại diện cho bán lẻ")
    else:
        print(f"   → KHUYẾN NGHỊ GIỮ outliers vì:")
        print(f"     • Chỉ chiếm {outlier_percent:.2f}% dữ liệu")
        print(f"     • Vẫn là giao dịch hợp lệ của doanh nghiệp")
    
    return outliers, outlier_threshold


def compare_top10_sellers_vs_revenue(df):
    """
    Phân tích 3: So sánh Top 10 Best Sellers vs Top 10 Highest Revenue
    """
    print("3. SO SÁNH TOP 10 BEST SELLERS VS HIGHEST REVENUE")
    
    # Lọc dữ liệu dương
    df_positive = df[df['Quantity'] > 0].copy()
    df_positive['Revenue'] = df_positive['Quantity'] * df_positive['UnitPrice']
    
    # Top 10 theo Quantity (Best Sellers)
    top10_qty = df_positive.groupby(['StockCode', 'Description']).agg({
        'Quantity': 'sum',
        'Revenue': 'sum'
    }).sort_values('Quantity', ascending=False).head(10)
    
    print("\nTop 10 Best Sellers (theo Quantity):")
    print(top10_qty.to_string())
    
    # Top 10 theo Revenue (Highest Revenue)
    top10_rev = df_positive.groupby(['StockCode', 'Description']).agg({
        'Quantity': 'sum',
        'Revenue': 'sum'
    }).sort_values('Revenue', ascending=False).head(10)
    
    print("\n\nTop 10 Highest Revenue (theo Revenue):")
    print(top10_rev.to_string())
    
    # So sánh
    common_items = set(top10_qty.index) & set(top10_rev.index)
    print(f"\n Số sản phẩm xuất hiện ở cả 2 danh sách: {len(common_items)}/10")
    if len(common_items) > 0:
        print("   Sản phẩm chung:")
        for item in common_items:
            print(f"   - {item[1]} ({item[0]})")
    
    # Vẽ biểu đồ cột chồng
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Biểu đồ 1: Top 10 Best Sellers
    ax1 = axes[0]
    x_pos = np.arange(len(top10_qty))
    
    # Chuẩn hóa để hiển thị trên cùng 1 trục
    qty_normalized = top10_qty['Quantity'] / top10_qty['Quantity'].max() * 100
    rev_normalized = top10_qty['Revenue'] / top10_qty['Revenue'].max() * 100
    
    width = 0.35
    ax1.bar(x_pos - width/2, qty_normalized, width, label='Quantity (chuẩn hóa)', color='#FF6B6B', alpha=0.8)
    ax1.bar(x_pos + width/2, rev_normalized, width, label='Revenue (chuẩn hóa)', color='#4ECDC4', alpha=0.8)
    
    ax1.set_xlabel('Sản phẩm', fontsize=11)
    ax1.set_ylabel('Giá trị chuẩn hóa (%)', fontsize=11)
    ax1.set_title('Top 10 Best Sellers - So sánh Quantity vs Revenue', fontsize=13, fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([desc[:30] + '...' if len(desc) > 30 else desc 
                         for code, desc in top10_qty.index], rotation=45, ha='right', fontsize=9)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Biểu đồ 2: Top 10 Highest Revenue
    ax2 = axes[1]
    x_pos = np.arange(len(top10_rev))
    
    qty_normalized = top10_rev['Quantity'] / top10_rev['Quantity'].max() * 100
    rev_normalized = top10_rev['Revenue'] / top10_rev['Revenue'].max() * 100
    
    ax2.bar(x_pos - width/2, qty_normalized, width, label='Quantity (chuẩn hóa)', color='#FF6B6B', alpha=0.8)
    ax2.bar(x_pos + width/2, rev_normalized, width, label='Revenue (chuẩn hóa)', color='#4ECDC4', alpha=0.8)
    
    ax2.set_xlabel('Sản phẩm', fontsize=11)
    ax2.set_ylabel('Giá trị chuẩn hóa (%)', fontsize=11)
    ax2.set_title('Top 10 Highest Revenue - So sánh Quantity vs Revenue', fontsize=13, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([desc[:30] + '...' if len(desc) > 30 else desc 
                         for code, desc in top10_rev.index], rotation=45, ha='right', fontsize=9)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('output/eda_top10_comparison.png', dpi=300, bbox_inches='tight')
    print("\n✓ Đã lưu biểu đồ: output/eda_top10_comparison.png")
    plt.close()
    
    # Phân tích insight
    print("\n INSIGHT:")
    print("   • Best Sellers: Sản phẩm bán chạy nhưng giá thấp (hàng phổ thông)")
    print("   • Highest Revenue: Sản phẩm tạo doanh thu cao (giá cao hoặc vừa bán chạy vừa giá cao)")
    if len(common_items) < 5:
        print("   → Sự khác biệt lớn: Sản phẩm bán chạy ≠ Sản phẩm tạo doanh thu cao")
    else:
        print("   → Có sự trùng lặp: Một số sản phẩm vừa bán chạy vừa tạo doanh thu cao")
    
    return top10_qty, top10_rev


def generate_final_report(df, country_stats, outlier_threshold):
    """
    Tạo báo cáo tổng hợp với các đề xuất ngưỡng lọc
    """
    print(" BÁO CÁO TỔNG HỢP VÀ ĐỀ XUẤT NGƯỠNG LỌC")
    
    uk_percent = country_stats.loc['United Kingdom', 'Trans_Percent']
    df_positive = df[df['Quantity'] > 0]
    outliers = df_positive[df_positive['Quantity'] > outlier_threshold]
    outlier_percent = len(outliers) / len(df_positive) * 100
    
    report = f"""

1. LỌC THEO COUNTRY:
    ĐỀ XUẤT: Chỉ giữ lại 'United Kingdom'
   
   LÝ DO:
   • UK chiếm {uk_percent:.1f}% tổng số giao dịch (áp đảo)
   • Dữ liệu đồng nhất về thị trường, văn hóa mua sắm
   • Giảm nhiễu từ các thị trường nhỏ khác ({len(country_stats)-1} quốc gia)
   • Phù hợp cho phân tích hành vi khách hàng địa phương
   
   CODE THỰC HIỆN:
   df_filtered = df[df['Country'] == 'United Kingdom']

2. LỌC THEO QUANTITY:
    ĐỀ XUẤT: {"Lọc bỏ outliers" if outlier_percent > 5 else "Giữ lại outliers"}
   
   LÝ DO:
   • Ngưỡng outlier: {outlier_threshold:.0f} (Q3 + 1.5*IQR)
   • Số đơn outlier: {len(outliers):,} ({outlier_percent:.2f}%)
   {"• Có thể là đơn bán buôn, không đại diện cho bán lẻ" if outlier_percent > 5 else "• Tỷ lệ nhỏ, vẫn là giao dịch hợp lệ"}
   
   CODE THỰC HIỆN:
   {"df_filtered = df_filtered[df_filtered['Quantity'] <= " + f"{outlier_threshold:.0f}]" if outlier_percent > 5 else "# Giữ nguyên, không lọc outliers"}

3. LỌC NEGATIVE QUANTITY (ĐƠN TRẢ HÀNG):
    ĐỀ XUẤT: Lọc bỏ đơn hàng có Quantity <= 0
   
   LÝ DO:
   • Quantity âm là đơn trả hàng/hủy
   • Không phù hợp cho phân tích mô hình bán hàng
   
   CODE THỰC HIỆN:
   df_filtered = df_filtered[df_filtered['Quantity'] > 0]

4. KẾT QUẢ SAU KHI LỌC:
   • Dữ liệu gốc: {len(df):,} dòng
   • Sau khi lọc UK: ~{int(len(df) * uk_percent / 100):,} dòng
   • Sau khi lọc Quantity > 0: ~{len(df_positive):,} dòng
   • Ước tính cuối cùng: ~{int(len(df_positive) * uk_percent / 100 * (1 - outlier_percent/100 if outlier_percent > 5 else 1)):,} dòng



def apply_filters(df):
    '''Áp dụng các ngưỡng lọc đề xuất từ EDA'''
    print(f"Dữ liệu gốc: {{len(df):,}} dòng")
    
    # Lọc 1: Chỉ giữ UK
    df = df[df['Country'] == 'United Kingdom']
    print(f"Sau khi lọc UK: {{len(df):,}} dòng")
    
    # Lọc 2: Bỏ đơn trả hàng
    df = df[df['Quantity'] > 0]
    print(f"Sau khi lọc Quantity > 0: {{len(df):,}} dòng")
    
    # Lọc 3: {"Bỏ outliers" if outlier_percent > 5 else "Giữ outliers"}
    {"df = df[df['Quantity'] <= " + f"{outlier_threshold:.0f}]" if outlier_percent > 5 else "# Không lọc outliers"}
    {"print(f\"Sau khi lọc outliers: {{len(df):,}} dòng\")" if outlier_percent > 5 else ""}
    
    return df

# Sử dụng:
df_clean = apply_filters(df)
"""
    
    print(report)
    
    # Lưu báo cáo ra file
    with open('output/eda_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print(" Đã lưu báo cáo: output/eda_report.txt")
    
    return report


def run_full_eda(input_file='src/data/dataset.xlsx'):
    """
    Chạy toàn bộ quy trình EDA
    """
       
    # Load dữ liệu
    df = load_data(input_file)
    
    # Phân tích 1: Country
    country_stats = analyze_country_distribution(df)
    
    # Phân tích 2: Quantity Outliers
    outliers, outlier_threshold = analyze_quantity_outliers(df)
    
    # Phân tích 3: Top 10 Comparison
    top10_qty, top10_rev = compare_top10_sellers_vs_revenue(df)
    
    # Tạo báo cáo tổng hợp
    report = generate_final_report(df, country_stats, outlier_threshold)
    
    print("\n" + "="*70)
    print(" HOÀN THÀNH PHÂN TÍCH EDA!")
    print("="*70)
    print("\n Các file output đã tạo:")
    print("   • output/eda_country_distribution.png - Phân bố theo quốc gia")
    print("   • output/eda_quantity_outliers.png - Phân tích outliers")
    print("   • output/eda_top10_comparison.png - So sánh Top 10")
    print("   • output/eda_report.txt - Báo cáo tổng hợp\n")
    
    return df, country_stats, outliers, outlier_threshold, top10_qty, top10_rev


if __name__ == "__main__":
    # Chạy EDA
    results = run_full_eda('src/data/dataset.xlsx')
