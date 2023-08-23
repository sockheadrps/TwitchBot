document.addEventListener('DOMContentLoaded', function () {
    const gifContainer = document.getElementById("gif-container");
    const folderCount = 5;
    const gifCount = 4;
    const displayDuration = 5000; // 5 seconds

    function displayGifFromFolder(folderIndex, gifIndex) {
        const gifElement = document.createElement("img");
        gifElement.src = `../gifs/${folderIndex + 1}/${gifIndex + 1}.gif`;

        gifContainer.innerHTML = ""; // Clear previous GIF
        gifContainer.appendChild(gifElement);

        setTimeout(() => {
            const nextGifIndex = (gifIndex + 1) % gifCount;
            if (nextGifIndex === 0) {
                const nextFolderIndex = (folderIndex + 1) % folderCount;
                displayGifFromFolder(nextFolderIndex, nextGifIndex);
            } else {
                displayGifFromFolder(folderIndex, nextGifIndex);
            }
        }, displayDuration);
    }

    // Start the loop from the first folder and first GIF
    displayGifFromFolder(0, 0);

});

