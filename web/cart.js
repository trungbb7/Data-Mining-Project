// Cart page functionality

async function initCart() {
    // Load data
    await Promise.all([loadProducts(), loadRecommendations()]);
    
    // Display cart
    displayCart();
}

function displayCart() {
    const cart = getCart();
    const cartItemsDiv = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');
    const recommendationsSection = document.getElementById('recommendations-section');
    
    if (cart.length === 0) {
        cartItemsDiv.innerHTML = `
            <div class="empty-cart">
                <p>Giỏ hàng trống</p>
                <a href="index.html" class="btn">Tiếp tục mua sắm</a>
            </div>
        `;
        cartSummary.style.display = 'none';
        recommendationsSection.style.display = 'none';
        return;
    }
    
    // Display cart items
    cartItemsDiv.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${formatPrice(item.price)}</div>
            </div>
            <button class="btn btn-danger" onclick="removeItem(${index})">Xóa</button>
        </div>
    `).join('');
    
    // Calculate and display total
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    document.getElementById('total-price').textContent = total.toFixed(2);
    cartSummary.style.display = 'block';
    
    // Display recommendations
    displayRecommendations(cart);
}

function displayRecommendations(cart) {
    const recommendationsSection = document.getElementById('recommendations-section');
    const recommendationsGrid = document.getElementById('recommendations-grid');
    
    const recommendedRules = getRecommendationsForCart(cart);
    
    if (recommendedRules.length === 0) {
        recommendationsSection.style.display = 'none';
        return;
    }
    
    recommendationsSection.style.display = 'block';
    
    // Get product details for recommendations
    const recommendedProducts = recommendedRules.map(rule => {
        // Find product in allProducts
        const product = allProducts.find(p => 
            p.name.toUpperCase() === rule.suggest.toUpperCase()
        );
        
        return {
            name: rule.suggest,
            price: product ? product.price : 0,
            expectedUtility: rule.expected_utility,
            basedOn: rule.input
        };
    });
    
    recommendationsGrid.innerHTML = recommendedProducts.map(product => `
        <div class="product-card">
            <div class="recommended-badge">GỢI Ý</div>
            <div class="product-icon">${getProductIcon()}</div>
            <div class="product-name">${product.name}</div>
            <div class="product-price">${formatPrice(product.price)}</div>
            <div class="utility-score">⭐ Điểm: ${product.expectedUtility.toLocaleString()}</div>
            <button class="btn" onclick='addRecommendedProduct(${JSON.stringify(product)})'>
                Thêm vào giỏ
            </button>
        </div>
    `).join('');
}

function removeItem(index) {
    removeFromCart(index);
    displayCart();
}

function addRecommendedProduct(product) {
    addToCart(product);
    displayCart();
}

function checkout() {
    const cart = getCart();
    if (cart.length === 0) {
        alert('Giỏ hàng trống!');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    alert(`✅ Đặt hàng thành công!\n\nTổng tiền: ${formatPrice(total)}\n\nCảm ơn bạn đã mua hàng!`);
    
    // Clear cart after checkout
    clearCart();
    displayCart();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initCart);
