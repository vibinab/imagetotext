const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const snap = document.getElementById('snap');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error('Error accessing webcam:', err);
    });

// Capture image
snap.addEventListener('click', () => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg');
   
    sendToFlask(dataUrl).then(() => {
        window.location.href = '/upload';
    });
   
});

function sendToFlask(dataUrl) {
    fetch('/upload', {
        method: 'POST',
        body: JSON.stringify({ image: dataUrl }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        document.getElementById('name').textContent =data.name 
        document.getElementById('date').textContent = data.date 
        document.getElementById('wordamount').textContent = data.wordamount
        document.getElementById('digitamount').textContent = data.digitamount
    })
    .catch(error => {
        console.error('Error:', error);
    });
}