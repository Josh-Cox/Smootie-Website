$vid_carousel = $('.vid-carousel')
    
$vid_carousel.flickity({
    cellAlign: 'left',
    wrapAround: true,
    freeScroll: true,
    imagesLoaded: true
})

$('.img-carousel').flickity({
    cellAlign: 'left',
    wrapAround: true,
    prevNextButtons: false,
    imagesLoaded: true,
    autoPlay: true
})

$('.circle-carousel').flickity({
    cellAlign: 'center',
    wrapAround: true,
    imagesLoaded: true,
    autoPlay: true,
    pageDots: false
})

$('.review-carousel').flickity({
    cellAlign: 'center',
    wrapAround: true,
    prevNextButtons: false,
    imagesLoaded: true
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
