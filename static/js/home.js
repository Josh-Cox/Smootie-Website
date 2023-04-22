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
    imagesLoaded: true
})

// stops videos/images getting cut off
$(document).ready(function(){
    $(".flickity-viewport").height("33rem");
});

function listener() {
    $(".flickity-viewport").height("33rem");
}

// bind event listener
$vid_carousel.on( 'select.flickity', listener);