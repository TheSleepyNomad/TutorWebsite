function delElStyleWidth(imgEl) {
    imgEl.style.removeProperty("width");
}
function delElStyleHight(imgEl) {
    imgEl.style.removeProperty("height");
}
function addClassForYoutubeDiv(videoEl) {
    videoEl.classList.add("padding-img")
    videoEl.classList.add("rounded")
}
function main (){
    let articleBlock = document.querySelector('.entry-single')
    let articleImages = articleBlock.querySelectorAll('.padding-img')
    let videoBlock = articleBlock.querySelectorAll('.youtube-embed-wrapper')
    for (let item = 0; item < articleImages.length; item++) {
        delElStyleWidth(articleImages[item]);
        delElStyleHight(articleImages[item]);
    }
    for (let item = 0; item < videoBlock.length; item++) {
        addClassForYoutubeDiv(videoBlock[item]);
    }
}

main()