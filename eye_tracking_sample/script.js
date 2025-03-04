document.getElementById("startTest").addEventListener("click", function() {
    document.getElementById("startScreen").classList.add("hidden");
    document.getElementById("eyeTrackingScreen").classList.remove("hidden");

    // Start Camera on Second Slide
    navigator.mediaDevices.getUserMedia({ video: true }) 
        .then(function(stream) {
            let videoElement = document.getElementById("video");
            videoElement.srcObject = stream;
        })
        .catch(function(error) {
            alert("Camera access denied. Please allow camera permissions in your browser.");
            console.error("Camera error:", error);
        });
});

document.getElementById("startTracking").addEventListener("click", function() {
    document.getElementById("eyeTrackingScreen").classList.add("hidden");
    document.getElementById("cameraAccessScreen").classList.remove("hidden");
});

document.getElementById("finishTest").addEventListener("click", function() {
    alert("Test Completed!");
});

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const socket = io("http://localhost:5000");

function sendFrame() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL("image/jpeg");
    socket.emit("video_frame", dataUrl);
}

socket.on("eye_tracking_data", (data) => {
    console.log("Received eye tracking data:", data);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    if (data.left_eye && data.right_eye) {
        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.arc(data.left_eye[0], data.left_eye[1], 5, 0, 2 * Math.PI);
        ctx.arc(data.right_eye[0], data.right_eye[1], 5, 0, 2 * Math.PI);
        ctx.fill();
    }
});

setInterval(sendFrame, 100);
