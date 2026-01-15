# AMAZECART
**This is a code for making the User Interface of a shopping app where a user can choose the item and add to cart the item.**
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AmazeCart - Electronics Shopping</title>
<style>
    * { margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI', sans-serif; }
    body { background:#f5f5f5; }
    header {
        background:#2874f0;
        color:white;
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:15px 30px;
        flex-wrap:wrap;
    }
    header h1 { font-size:28px; font-weight:700; }
    nav a {
        color:white; text-decoration:none; margin:0 10px; font-weight:600;
    }
    nav a:hover { text-decoration:underline; }

    .search-bar {
        margin:10px auto;
        display:flex;
        justify-content:center;
        align-items:center;
    }
    .search-bar input {
        width:300px; padding:8px; border:1px solid #ccc; border-radius:4px 0 0 4px;
    }
    .search-bar button {
        background:#2874f0; color:white; border:none; padding:9px 15px; border-radius:0 4px 4px 0; cursor:pointer;
    }

    .product-list {
        display:flex; flex-wrap:wrap; gap:20px; justify-content:center; padding:20px;
    }
    .product {
        background:white; width:230px; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.1);
        text-align:center; padding:15px; transition:transform .2s;
    }
    .product:hover { transform:scale(1.03); }
    .product img { width:100%; height:160px; object-fit:contain; }
    .product h3 { margin:10px 0; font-size:18px; color:#333; }
    .product p { color:#666; font-size:14px; }
    .product .price { color:#2874f0; font-size:16px; font-weight:bold; margin:5px 0; }
    .buttons { display:flex; justify-content:space-around; margin-top:10px; }
    button {
        background:#2874f0; color:white; border:none; border-radius:5px;
        padding:7px 10px; cursor:pointer; font-size:13px;
    }
    button:hover { background:#0a58ca; }
    footer {
        background:#222; color:white; text-align:center; padding:15px; margin-top:30px;
    }
    #cart-section, #like-section, #contact-section { display:none; padding:20px; }
    #cart-items, #like-items { background:white; border-radius:10px; padding:15px; }
    .product-detail { font-size:13px; color:#555; }
    h2 { text-align:center; margin:15px 0; color:#333; }
    .contact-info { text-align:center; line-height:1.8; background:white; padding:15px; border-radius:10px; }
    .highlight { color:#2874f0; font-weight:bold; }
</style>
</head>
<body>

<header>
    <h1>🛒 AmazeCart</h1>
    <nav>
        <a href="#" id="homeLink">Home</a>
        <a href="#" id="cartLink">Cart (<span id="cart-count">0</span>)</a>
        <a href="#" id="likeLink">Liked Items (<span id="like-count">0</span>)</a>
        <a href="#" id="contactLink">Contact</a>
    </nav>
</header>

<div class="search-bar">
    <input type="text" id="searchBox" placeholder="Search electronics...">
    <button onclick="searchProducts()">Search</button>
</div>

<!-- Home Section -->
<section id="product-section">
    <h2>Electronics Collection</h2>
    <div class="product-list"></div>
</section>

<!-- Cart Section -->
<section id="cart-section">
    <h2>Your Cart</h2>
    <div id="cart-items"></div>
    <h3 id="total">Total: ₹0</h3>
    <button id="clear-cart">Clear Cart</button>
</section>

<!-- Liked Items Section -->
<section id="like-section">
    <h2>Liked Items</h2>
    <div id="like-items"></div>
</section>

<!-- Contact Section -->
<section id="contact-section">
    <h2>Contact Us</h2>
    <div class="contact-info">
        <p>📞 Call us at:</p>
        <p class="highlight">+91 90000 00001 | +91 90000 00002 | +91 90000 00003</p>
        <p>📧 Email: support@amazecart.com</p>
        <p>📍 Address: 123 AmazeCart Plaza, Mumbai, India</p>
        <p>© 2025 AmazeCart | Designed by Student</p>
    </div>
</section>

<footer>
    <p>© 2025 AmazeCart | All Rights Reserved</p>
</footer>

<script>
const products = [
    { id:1, name:"Apple iPhone 15", brand:"Apple", price:79999, image:"https://en.wikipedia.org/wiki/IPhone_15#/media/File:IPhone_15_Vector.svg", details:"128GB storage, A16 Bionic chip, Dual camera system." },
    { id:2, name:"Samsung Galaxy S23", brand:"Samsung", price:74999, image:"https://en.wikipedia.org/wiki/Samsung_Galaxy_S23#/media/File:Galaxy_S23.png", details:"256GB storage, Snapdragon 8 Gen 2, AMOLED display." },
    { id:3, name:"Hp pavilion laptop", brand:"HP", price:55999, image:"https://en.wikipedia.org/wiki/HP_Pavilion#/media/File:HP_Pavilion_15_cs3095nr.png", details:"Intel i5 12th Gen, 16GB RAM, 512GB SSD, Windows 11." },
    { id:4, name:"Dell Inspiron 15", brand:"Dell", price:62999, image:"https://en.wikipedia.org/wiki/Dell_Inspiron_laptops#/media/File:Dell_Inspiron_3500.jpg", details:"Ryzen 5, 8GB RAM, 1TB HDD, Full HD Display." },
    { id:5, name:"Sony WH-1000XM5 Headphones", brand:"Sony", price:29999, image:"https://en.wikipedia.org/wiki/Headphones#/media/File:S%C5%82uchawki_referencyjne_K-701_firmy_AKG.jpg", details:"Noise-cancelling wireless headphones, 30 hrs battery." },
    { id:6, name:"OnePlus Smart TV 43\"", brand:"OnePlus", price:28999, image:"https://en.wikipedia.org/wiki/OnePlus#/media/File:OnePlus_One.png", details:"43-inch Full HD Smart LED TV with Android OS." },
    { id:7, name:"Lenovo IdeaPad 3", brand:"Lenovo", price:47999, image:"https://en.wikipedia.org/wiki/IdeaPad#/media/File:Lenovo_IdeaPad_320.jpg", details:"Intel i5, 8GB RAM, 512GB SSD, 15.6-inch display." },
    { id:8, name:"Boat Rockerz 450", brand:"Boat", price:1499, image:"https://en.wikipedia.org/wiki/Headphones#/media/File:GradoPrestige-HeadphoneArticle.jpg", details:"Bluetooth wireless headphones, 15 hrs playtime." },
    { id:9, name:"Canon EOS 200D II", brand:"Canon", price:58999, image:"https://en.wikipedia.org/wiki/Canon_Inc.#/media/File:Canon_FTb_with_50mm_F-1.8_lens.jpg", details:"24.1MP DSLR camera, Dual Pixel CMOS AF, Wi-Fi." },
    { id:10, name:"Realme Narzo 60", brand:"Realme", price:17999, image:"https://en.wikipedia.org/wiki/Smartphone#/media/File:Blackview_A60_Smartphone_Android_mobile_phone_front_face_logged_in_screen.jpg", details:"8GB RAM, 128GB storage, 64MP camera, 5G support." }
];

let cart = [];
let likes = [];

// Display all products
function displayProducts(list=products) {
    const container = document.querySelector(".product-list");
    container.innerHTML = "";
    list.forEach(p => {
        const card = document.createElement("div");
        card.classList.add("product");
        card.innerHTML = `
            <img src="${p.image}" alt="${p.name}">
            <h3>${p.name}</h3>
            <p class="product-detail">${p.details}</p>
            <p class="price">₹${p.price}</p>
            <div class="buttons">
                <button onclick="addToCart(${p.id})">Add to Cart</button>
                <button onclick="likeItem(${p.id})">❤️ Like</button>
            </div>
            <button onclick="buyItem(${p.id})">Buy Now</button>
        `;
        container.appendChild(card);
    });
}

// Add item to cart
function addToCart(id){
    const item = products.find(p=>p.id===id);
    const found = cart.find(c=>c.id===id);
    if(found){found.quantity+=1;} else {cart.push({...item,quantity:1});}
    updateCartCount();
    alert(`${item.name} added to cart!`);
}

// Like item
function likeItem(id){
    const item = products.find(p=>p.id===id);
    if(!likes.find(l=>l.id===id)){
        likes.push(item);
        alert(`${item.name} added to Liked Items!`);
    }
    updateLikeCount();
}

// Show cart
function showCart(){
    showSection("cart-section");
    const container=document.getElementById("cart-items");
    container.innerHTML="";
    let total=0;
    cart.forEach(i=>{
        total+=i.price*i.quantity;
        container.innerHTML+=`<p>${i.name} (x${i.quantity}) - ₹${i.price*i.quantity}</p>`;
    });
    document.getElementById("total").textContent=`Total: ₹${total}`;
}

// Show liked items
function showLikes(){
    showSection("like-section");
    const container=document.getElementById("like-items");
    container.innerHTML="";
    likes.forEach(i=>{
        container.innerHTML+=`<p>${i.name} - ₹${i.price}</p>`;
    });
}

// Buy item
function buyItem(id){
    const item = products.find(p=>p.id===id);
    alert(`Thank you for buying ${item.name}!\nOur team will contact you for delivery.`);
}

// Clear cart
document.getElementById("clear-cart").addEventListener("click", ()=>{
    cart=[];
    updateCartCount();
    showCart();
});

// Search function
function searchProducts(){
    const query=document.getElementById("searchBox").value.toLowerCase();
    const filtered=products.filter(p=>p.name.toLowerCase().includes(query)||p.brand.toLowerCase().includes(query));
    displayProducts(filtered);
}

// Navigation
document.getElementById("homeLink").addEventListener("click", ()=>showSection("product-section"));
document.getElementById("cartLink").addEventListener("click", showCart);
document.getElementById("likeLink").addEventListener("click", showLikes);
document.getElementById("contactLink").addEventListener("click", ()=>showSection("contact-section"));

// Helpers
function showSection(id){
    document.getElementById("product-section").style.display="none";
    document.getElementById("cart-section").style.display="none";
    document.getElementById("like-section").style.display="none";
    document.getElementById("contact-section").style.display="none";
    document.getElementById(id).style.display="block";
}

function updateCartCount(){ document.getElementById("cart-count").textContent=cart.reduce((s,i)=>s+i.quantity,0); }
function updateLikeCount(){ document.getElementById("like-count").textContent=likes.length; }

displayProducts();
</script>
</body>
</html>
