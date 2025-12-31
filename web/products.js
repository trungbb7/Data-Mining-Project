// Global variables
let allProducts = [];
let recommendations = [];

// Load products from CSV
async function loadProducts() {
    try {
        const response = await fetch('../output/products_with_price.csv');
        const text = await response.text();
        
        const lines = text.split('\n');
        const products = [];
        
        // Skip header and parse CSV
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;
            
            // Parse CSV line (handle commas in product names)
            const lastCommaIndex = line.lastIndexOf(',');
            if (lastCommaIndex === -1) continue;
            
            const description = line.substring(0, lastCommaIndex).trim();
            const price = parseFloat(line.substring(lastCommaIndex + 1).trim());
            
            if (description && !isNaN(price)) {
                products.push({
                    name: description,
                    price: price
                });
            }
        }
        
        allProducts = products;
        return products;
    } catch (error) {
        console.error('Error loading products:', error);
        return [];
    }
}

// Load recommendation rules from JSON
async function loadRecommendations() {
    try {
        const response = await fetch('../output/recommendation_rules.json');
        recommendations = await response.json();
        return recommendations;
    } catch (error) {
        console.error('Error loading recommendations:', error);
        return [];
    }
}

// Get unique products (remove duplicates)
function getUniqueProducts(products) {
    const uniqueMap = new Map();
    
    products.forEach(product => {
        const key = product.name.toUpperCase();
        if (!uniqueMap.has(key)) {
            uniqueMap.set(key, product);
        }
    });
    
    return Array.from(uniqueMap.values());
}

// Get random product icon
function getProductIcon() {
    const icons = ['🎁', '📦', '🎀', '🎨', '🏺', '🎪', '🎭', '🎯', '🎲', '🧸', '🎸', '📚', '☕', '🍰', '🎂', '🍪', '🧁', '🎈', '🎉', '🎊'];
    return icons[Math.floor(Math.random() * icons.length)];
}

// Cart management
function getCart() {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function addToCart(product) {
    const cart = getCart();
    cart.push(product);
    saveCart(cart);
    alert(`✅ Đã thêm "${product.name}" vào giỏ hàng!`);
}

function removeFromCart(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
}

function clearCart() {
    localStorage.removeItem('cart');
    updateCartCount();
}

function updateCartCount() {
    const cart = getCart();
    const countElements = document.querySelectorAll('#cart-count');
    countElements.forEach(el => {
        el.textContent = cart.length;
    });
}

// Get recommendations based on cart items
function getRecommendationsForCart(cart) {
    if (!cart || cart.length === 0 || !recommendations || recommendations.length === 0) {
        return [];
    }
    
    // Get product names in cart
    const cartProductNames = cart.map(p => p.name.toUpperCase());
    
    // Find matching rules
    const matchingRules = recommendations.filter(rule => {
        // Check if all items in rule.input are in cart
        return rule.input.every(inputItem => 
            cartProductNames.includes(inputItem.toUpperCase())
        );
    });
    
    // Sort by expected_utility and get unique suggestions
    const suggestions = new Map();
    
    matchingRules.forEach(rule => {
        const suggestName = rule.suggest.toUpperCase();
        
        // Don't suggest items already in cart
        if (cartProductNames.includes(suggestName)) {
            return;
        }
        
        // Keep the rule with highest utility for each product
        if (!suggestions.has(suggestName) || 
            suggestions.get(suggestName).expected_utility < rule.expected_utility) {
            suggestions.set(suggestName, rule);
        }
    });
    
    // Convert to array and sort by utility
    return Array.from(suggestions.values())
        .sort((a, b) => b.expected_utility - a.expected_utility)
        .slice(0, 6); // Limit to top 6 recommendations
}

// Format price
function formatPrice(price) {
    return `£${price.toFixed(2)}`;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
});
