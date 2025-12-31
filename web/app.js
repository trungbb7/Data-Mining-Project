// Main app for products page
let displayedProducts = [];

// Initialize the app
async function init() {
    const productsGrid = document.getElementById('products-grid');
    productsGrid.innerHTML = '<div class="loading">Đang tải sản phẩm...</div>';
    
    // Load data
    await Promise.all([loadProducts(), loadRecommendations()]);
    
    if (allProducts.length === 0) {
        productsGrid.innerHTML = '<div class="loading">Không thể tải danh sách sản phẩm</div>';
        return;
    }
    
    // Display products
    displayProducts();
    
    // Setup event listeners
    setupEventListeners();
}

function displayProducts(filter = '') {
    const productsGrid = document.getElementById('products-grid');
    const showUnique = document.getElementById('show-unique').checked;
    
    // Get products to display
    let products = showUnique ? getUniqueProducts(allProducts) : allProducts;
    
    // Apply search filter
    if (filter) {
        const filterLower = filter.toLowerCase();
        products = products.filter(p => 
            p.name.toLowerCase().includes(filterLower)
        );
    }
    
    displayedProducts = products;
    updateProductCount();
    
    // Render products
    if (products.length === 0) {
        productsGrid.innerHTML = '<div class="loading">Không tìm thấy sản phẩm nào</div>';
        return;
    }
    
    productsGrid.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-icon">${getProductIcon()}</div>
            <div class="product-name">${product.name}</div>
            <div class="product-price">${formatPrice(product.price)}</div>
            <button class="btn" onclick='addProductToCart(${JSON.stringify(product)})'>
                Thêm vào giỏ
            </button>
        </div>
    `).join('');
}

function updateProductCount() {
    const countEl = document.getElementById('product-count');
    if (countEl) {
        countEl.textContent = `Hiển thị ${displayedProducts.length} sản phẩm`;
    }
}

function addProductToCart(product) {
    addToCart(product);
}

function setupEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            displayProducts(e.target.value);
        });
    }
    
    // Show unique checkbox
    const showUniqueCheckbox = document.getElementById('show-unique');
    if (showUniqueCheckbox) {
        showUniqueCheckbox.addEventListener('change', () => {
            const searchValue = searchInput ? searchInput.value : '';
            displayProducts(searchValue);
        });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);
