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
    document.getElementById("rating").textContent = data.rating;
    document.getElementById("comments").textContent = data.comments || "No comments";
    document.getElementById("diseaseName").textContent = data.disease_name;
    document.getElementById("image").src = `${backendUrl}/${data.image_path}`; // Use the full path from the backend
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
      document.getElementById("rating").textContent = data.rating;
      document.getElementById("comments").textContent = data.comments || "No comments";
      document.getElementById("diseaseName").textContent = data.disease_name;
      document.getElementById("image").src = `${backendUrl}/${data.image_path}`; // Use the full path from the backend
      currentImageId = data.id;
    } catch (error) {
      console.error("Fetch error:", error);
    }
  } else {
    await loadImage(null);
  }
}

// Load the first image when the page loads
window.onload = () => {
  loadImage(null);
};

// Add event listener to your "Next" button
document.getElementById("nextButton").addEventListener("click", loadNextImage);