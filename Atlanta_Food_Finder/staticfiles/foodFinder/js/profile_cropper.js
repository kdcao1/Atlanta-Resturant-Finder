const profileImagePreview = document.getElementById('profileImagePreview');
const profilePictureInput = document.getElementById('profilePictureInput');
const croppedImageData = document.getElementById('croppedImageData');
const resetButton = document.getElementById('resetButton');
let cropper;

// Variable to store the original image and the last cropped image
let originalImageSrc;
let lastCroppedImage;

// Initialize Cropper.js when the page loads
window.onload = function () {
    originalImageSrc = profileImagePreview.src;  // Store the initial profile picture URL
    cropper = new Cropper(profileImagePreview, {
        aspectRatio: 1, // Square crop
        viewMode: 1, // Restrict the image within the crop box
        scalable: true, // Allow image scaling
        zoomable: true, // Allow zooming
    });
};

// Update image preview and replace the cropper image on file selection
profilePictureInput.addEventListener('change', function (event) {
    const reader = new FileReader();
    reader.onload = function (e) {
        profileImagePreview.src = e.target.result; // Update image preview
        if (cropper) {
            cropper.replace(e.target.result); // Replace the image in the cropper
            lastCroppedImage = null; // Reset the last cropped image reference
        }
    };
    reader.readAsDataURL(event.target.files[0]);
});

// Handle Reset button click
resetButton.addEventListener('click', function() {
    if (lastCroppedImage) {
        // If a cropped image exists, set the preview to that image
        profileImagePreview.src = lastCroppedImage; // Set the preview to the last cropped image
        cropper.replace(lastCroppedImage); // Replace the cropper image with the last cropped image
    } else {
        // If no cropped image exists, reset to the original upload
        profileImagePreview.src = originalImageSrc; // Reset to the original image
        cropper.replace(originalImageSrc); // Reset the cropper with the original image
    }
});

// Before form submission, convert cropped image to base64 and set hidden input value
document.querySelector('form').addEventListener('submit', function (event) {
    if (cropper) {
        const croppedCanvas = cropper.getCroppedCanvas({
            width: 128, // Output size
            height: 128,
        });
        lastCroppedImage = croppedCanvas.toDataURL('image/png'); // Store the last cropped image
        croppedImageData.value = lastCroppedImage; // Convert to base64 and set hidden input value
    }
});
