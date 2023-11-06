document.addEventListener('DOMContentLoaded', function () {
    // Add an event listener to the file input to handle the selected image
    document.querySelector('#imageUpload').addEventListener('change', function () {
        // Get the selected image file
        const selectedImage = this.files[0];

        // Reference to the target <div> where you want to display the image
        const imageContainer = document.getElementById('uploadedImageContainer');

        // Create an <img> element to display the selected image
        const imageElement = document.createElement('img');
        imageElement.width = 300; // Set the width to match the existing SVG
        imageElement.height = 300; // Set the height to match the existing SVG

        if (selectedImage) {
            // Set the selected image as the source
            imageElement.src = URL.createObjectURL(selectedImage);

            // Clear the existing SVG content
            imageContainer.innerHTML = '';

            // Append the <img> element to the container
            imageContainer.appendChild(imageElement);
        }
    });
});
