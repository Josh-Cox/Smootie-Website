
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
let color_text_elements = document.querySelectorAll(".color-selected");
let add_cart_button = document.getElementById("submit-button");

$("input:radio[name=color]").change(function() {
    color_text_elements.forEach((element) => {
        element.innerText = ("Colour: " + this.value);
    })
    add_cart_button.setAttribute("data-product", this.getAttribute("productId"));

    // span of each color button
    let color_buttons = document.querySelectorAll(".circle-outer");
    let x = window.matchMedia("(max-width: 600px)")
    color_buttons.forEach(function(item) {
        item.style.width = ".1rem";
        item.style.height = ".1rem";
    });

    if (x.matches) {
        this.parentElement.childNodes[3].style.width = "2.3rem";
        this.parentElement.childNodes[3].style.height = "2.3rem";
    } else {
        this.parentElement.childNodes[3].style.width = "1.9rem";
        this.parentElement.childNodes[3].style.height = "1.9rem";
    }
    

    
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


let gallery_images = document.querySelectorAll(".gallery-image-img");
let gallery_selected = document.querySelector(".gallery-selected-img");

// image selection
gallery_images.forEach(function(image) {
    image.addEventListener("click", function () {
        $(".gallery-selected-img")
        .fadeOut(300, function() {
            $(".gallery-selected-img").attr('src', image.src);
        })
        .fadeIn(300);
    });
});

// tab selection
let tab_headers = document.querySelectorAll('.tab-header');
let tab_contents = document.querySelectorAll('.tab-content');

tab_headers.forEach(function(header) {
    header.addEventListener("click", function() {
        tab_headers.forEach(function(item) {
            item.classList.remove("active");
        })

        tab_contents.forEach(function(item) {
            item.classList.remove("active");
        })

        let temp_id = "." + header.id;

        document.querySelector(temp_id).classList.add("active");
        header.classList.add("active");
    });
}); 

// function selection
let function_icons = document.querySelectorAll('.function-icon');
let function_content = document.querySelectorAll('.function-info');

function_icons.forEach(function(header) {
    header.addEventListener("click", function() {
        function_icons.forEach(function(item) {
            item.classList.remove("active");
        })

        function_content.forEach(function(item) {
            item.classList.remove("active");
        })

        let temp_id = "." + header.id;

        document.querySelector(temp_id).classList.add("active");
        header.classList.add("active");
    });
}); 



// faq section
const dropdown = document.querySelectorAll('.drop-down-question');

dropdown.forEach(dropdown => {
    dropdown.addEventListener('click', () => {
        let content = dropdown.childNodes[3];
        let heading = dropdown.childNodes[1].childNodes[3];
        content.classList.toggle('active');
        heading.classList.toggle('active');
    });
});

// color picker change image
$("input:radio[value=White]").change(function() {

    mainImage.src = document.getElementById("white-img").src;
    
    document
        .querySelector(".product__image--active")
        .classList.remove("product__image--active");
    
    document.getElementById("white-img").classList.add("product__image--active");
});

$("input:radio[value=Pink]").change(function() {

    mainImage.src = document.getElementById("pink-img").src;
    
    document
        .querySelector(".product__image--active")
        .classList.remove("product__image--active");
    
    document.getElementById("pink-img").classList.add("product__image--active");
});

$("input:radio[value=Black]").change(function() {

    mainImage.src = document.getElementById("black-img").src;
    
    document
        .querySelector(".product__image--active")
        .classList.remove("product__image--active");
    
    document.getElementById("black-img").classList.add("product__image--active");
});

$("input:radio[value=Yellow]").change(function() {

    mainImage.src = document.getElementById("yellow-img").src;
    
    document
        .querySelector(".product__image--active")
        .classList.remove("product__image--active");
    
    document.getElementById("yellow-img").classList.add("product__image--active");
});

$('.img-carousel').flickity({
    cellAlign: 'center',
    wrapAround: true,
    prevNextButtons: false,
    imagesLoaded: true,
    autoPlay: true
})

$vid_carousel = $('.vid-carousel')
    
$vid_carousel.flickity({
    cellAlign: 'center',
    wrapAround: true,
    freeScroll: true,
    groupCells: 2,
    imagesLoaded: true
})

$('.review-carousel').flickity({
    cellAlign: 'center',
    wrapAround: true,
    prevNextButtons: false,
    imagesLoaded: true,
    autoPlay: true
})

// stops videos/images getting cut off
let x = window.matchMedia("(max-width: 600px)")

if (x.matches) {
    $(document).ready(function(){
        $(".flickity-viewport").height("19rem");
    });
} else {
    $(document).ready(function(){
        $(".flickity-viewport").height("37rem");
    });
}

// video custom play button
let playButtons = document.querySelectorAll(".vid-btn");
// Event listener for the play/pause button

playButtons.forEach(btn => {
    btn.addEventListener("click", function() {
        if (btn.previousElementSibling.paused == true) {
          // Play the video
          btn.previousElementSibling.play();
      
          // Update the button text to 'Pause'
          btn.childNodes[1].innerHTML = "pause_circle";
        } else {
          // Pause the video
          btn.previousElementSibling.pause();
      
          // Update the button text to 'Play'
          btn.childNodes[1].innerHTML = "play_circle";
        }
    });
});