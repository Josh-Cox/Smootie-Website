
// product images
const mainImage = document.getElementById("main-image");
const images = document.querySelectorAll(".product__image");

images.forEach((image) => {
    image.addEventListener("click", (event) => {
        mainImage.src = event.target.src;

        document
            .querySelector(".product__image--active")
            .classList.remove("product__image--active");

        event.target.classList.add("product__image--active");
    });
});

// color picker, product ID
let color_text = document.getElementById("color-text");
let add_cart_button = document.getElementById("submit-button");

$("input:radio[name=color]").change(function() {
    color_text.innerText = ("Colour: " + this.value);
    add_cart_button.setAttribute("data-product", this.getAttribute("productId"));
});

// quantity picker
let quantity_btns = document.querySelectorAll(".quantity-update");
let quantity = document.querySelector(".quantity-number");
let data_quant = document.querySelector(".add-cart-btn");

quantity_btns.forEach(function(btn) {
    btn.addEventListener("click", function() {
        let original = $(".quantity-number").attr("value");
        if(btn.getAttribute("action") == "add") {
            $(".quantity-number").attr("value", parseInt(original) + 1);
        }
        else if((btn.getAttribute("action") == "remove") && (parseInt($(".quantity-number").attr("value"))) > 1) {
            $(".quantity-number").attr("value", parseInt(original) - 1);
        }

        $(".quantity-number").text($(".quantity-number").attr("value"));
        data_quant.setAttribute("data-quantity", $(".quantity-number").attr("value"));
    });
});

// function active on click
let icons = document.querySelectorAll(".function-icon");

icons.forEach(function(icon) {
    icon.addEventListener("click", function() {
        icons.forEach(function(item) {
            item.classList.remove("active");
        });

        icon.classList.add("active");
    });
});