const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const toggleCameraButton = document.getElementById("toggle-camera");
const toggleUploadButton = document.getElementById("toggle-upload");
const cameraContainer = document.getElementById("camera-container");
const cameraView = document.getElementById("camera-view");
const capturedPhoto = document.getElementById("captured-photo");
const uploadSection = document.querySelector(".upload");
const takePhotoButton = document.getElementById("take-photo");
const capturedImageData = document.getElementById("captured-image-data");
const resultDiv = document.getElementById("result"); // Kết quả dự đoán

let mediaStream;
let photoCaptured = false;

cameraContainer.style.display = "none";
toggleUploadButton.style.display = "none";
takePhotoButton.style.display = "none"; // Initially hide the "Chụp Ảnh" button

let cameraActive = false;

function clearPredictionResult() {
  if (resultDiv) {
    resultDiv.innerHTML = ""; // Xóa nội dung của kết quả dự đoán
    resultDiv.classList.remove("coconut-result");
  }
}

function clearUploadedImage() {
  imageView.innerHTML = `
    <img src="/static/iconupload.png">
    <p>Kéo và thả hoặc bấm vào đây<br>để tải ảnh lên</p>
  `;
  clearPredictionResult(); // Xóa kết quả dự đoán khi tải ảnh mới lên
}

toggleCameraButton.addEventListener("click", function () {
  if (!cameraActive) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        cameraView.srcObject = stream;
        mediaStream = stream;
        cameraActive = true;

        toggleCameraButton.style.display = "none";
        toggleUploadButton.style.display = "inline";

        uploadSection.style.display = "none";

        cameraView.style.display = "block";
        capturedPhoto.style.display = photoCaptured ? "block" : "none";
        takePhotoButton.style.display = "block"; // Show the "Chụp Ảnh" button

        cameraContainer.style.display = "flex";
        clearPredictionResult(); // Xóa kết quả dự đoán khi chuyển sang chế độ bật camera
      })
      .catch((error) => {
        console.error('Error accessing the camera:', error);
      });
  } else {
    mediaStream.getTracks().forEach((track) => track.stop());
    cameraActive = false;

    toggleCameraButton.style.display = "inline";
    toggleUploadButton.style.display = "none";
    takePhotoButton.style.display = "none"; // Hide the "Chụp Ảnh" button

    cameraContainer.style.display = "none";
    clearPredictionResult(); // Xóa kết quả dự đoán khi chuyển sang chế độ tải ảnh
  }
});

toggleUploadButton.addEventListener("click", function () {
  clearUploadedImage();
  inputFile.value = "";

  capturedPhoto.src = "";
  capturedPhoto.style.display = "none";
  photoCaptured = false;

  cameraContainer.style.display = "none";
  uploadSection.style.display = "flex";

  if (cameraActive) {
    mediaStream.getTracks().forEach((track) => track.stop());
    cameraActive = false;
  }

  toggleCameraButton.style.display = "inline";
  toggleUploadButton.style.display = "none";
  takePhotoButton.style.display = "none"; // Hide the "Chụp Ảnh" button
});

inputFile.addEventListener("change", uploadImage);

function uploadImage() {
  let imgLink = URL.createObjectURL(inputFile.files[0]);
  imageView.innerHTML = `<img src="${imgLink}">`;
  capturedImageData.value = imgLink;
  clearPredictionResult(); // Xóa kết quả dự đoán khi bạn tải ảnh mới lên
}

takePhotoButton.addEventListener('click', function () {
  if (!photoCaptured) {
    if (cameraActive) {
      const canvas = document.createElement('canvas');
      canvas.width = cameraView.videoWidth;
      canvas.height = cameraView.videoHeight;
      const context = canvas.getContext('2d');
      context.drawImage(cameraView, 0, 0, canvas.width, canvas.height);

      capturedPhoto.src = canvas.toDataURL('image/jpeg');
      capturedImageData.value = capturedPhoto.src;

      capturedPhoto.style.display = "block";
      cameraView.style.display = "none";
      photoCaptured = true;
      clearPredictionResult(); // Xóa kết quả dự đoán khi bạn chụp ảnh
    }
  } else {
    capturedPhoto.src = "";
    capturedPhoto.style.display = "none";
    cameraView.style.display = "block";
    photoCaptured = false;
    clearPredictionResult(); // Xóa kết quả dự đoán khi bạn chụp ảnh
  }
});

dropArea.addEventListener("dragover", function (e) {
  e.preventDefault();
});

dropArea.addEventListener("drop", function (e) {
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadImage();
});

const logoutButton = document.getElementById("logoutButton");

logoutButton.addEventListener("click", () => {
  window.location.href = '/logout';
});
