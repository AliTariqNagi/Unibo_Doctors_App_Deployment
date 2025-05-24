let currentImageId = null;
const backendUrl = "http://localhost:8000"; // Define your backend URL

async function loadImage(imageId) {
  let url = `${backendUrl}/first_image/`;
  if (imageId !== null) {
    url = `${backendUrl}/doctor_image_validation/${imageId}`; // Use the correct backend route
  }
  try {
    const response = await fetch(url);
    if (!response.ok) {
      const error = await response.json();
      console.error("Error loading image:", error);
      return;
    }
    const data = await response.json();
    document.getElementById("doctorName").textContent = data.doctor_name;
    document.getElementById("rating-display").textContent = data.rating;
    document.getElementById("comments-display").textContent = data.comments || "No comments";
    document.getElementById("diseaseName-display").textContent = data.disease_name;
    document.getElementById("image").src = `${backendUrl}/images/${data.image_path.split('/').pop()}`; // Correct image URL
    currentImageId = data.id;
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

async function loadNextImage() {
  if (currentImageId !== null) {
    try {
      const response = await fetch(`${backendUrl}/next_image/${currentImageId}`);
      if (!response.ok) {
        const error = await response.json();
        if (response.status === 404) {
          alert("No more images!");
        } else {
          console.error("Error loading next image:", error);
        }
        return;
      }
      const data = await response.json();
      document.getElementById("doctorName").textContent = data.doctor_name;
      document.getElementById("rating-display").textContent = data.rating;
      document.getElementById("comments-display").textContent = data.comments || "No comments";
      document.getElementById("diseaseName-display").textContent = data.disease_name;
      document.getElementById("image").src = `${backendUrl}/images/${data.image_path.split('/').pop()}`; // Correct image URL
      currentImageId = data.id;
    } catch (error) {
      console.error("Fetch error:", error);
    }
  } else {
    await loadImage(null);
  }
}

// Initially, you might not want to load an image on page load if the form is the primary focus.
// If you still want to load the first image, keep this:
window.onload = () => {
  // Hide the image container initially
  document.getElementById('image-container').style.display = 'none';
  // You might want a button to trigger the image viewing section
  // loadImage(null); // Uncomment this if you want to load the first image initially
};

// Add event listener to your "Next" button (assuming you still want image viewing)
const nextButton = document.getElementById("nextButton");
if (nextButton) {
    nextButton.addEventListener("click", loadNextImage);
}

// Functionality to show the image viewing section (you'll need a trigger for this)
function showImageViewer() {
    document.getElementById('validation-form').style.display = 'none';
    document.getElementById('image-container').style.display = 'block';
    loadImage(null); // Load the first image when the viewer is shown
}

// You'll need a button or some other mechanism in your HTML to call showImageViewer()
// For example: <button onclick="showImageViewer()">View Images</button>