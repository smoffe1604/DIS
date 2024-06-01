document.addEventListener('DOMContentLoaded', function() {
    const image = document.querySelector('.spinning-image');
    positionImage(image);


    // To stop the spinning
    function stopSpinning() {
        image.style.animationPlayState = 'paused';
    }

    // To start the spinning
    function startSpinning() {
        image.style.animationPlayState = 'running';
    }

    function positionImage(img) {
        img.onload = function() {
            const maxX = window.innerWidth - img.width;
            const maxY = window.innerHeight - img.height;
    
            // Ensure that randomX and randomY are declared and initialized before use
            const randomX = Math.floor(Math.random() * maxX);
            const randomY = Math.floor(Math.random() * maxY);
    
            // Use randomX and randomY after their declaration
            img.style.left = randomX + 'px';
            img.style.top = randomY + 'px';
        }
    
        // If the image is already loaded and dimensions are known, you need to trigger the positioning
        if (img.complete) {
            img.onload();
        }
    }

    // Example usage
    //stopSpinning(); // Call this function to stop spinning
    //startSpinning(); // Call this function to start spinning again
});

    
