let socket = new WebSocket('ws://localhost:8888/websocket');

document.addEventListener('DOMContentLoaded', () => {
    let canvas = document.getElementById('canvas');
    let context = canvas.getContext('2d');
    const video = document.querySelector("#videoElement");

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({video: true}).then(function (stream) {
                video.srcObject = stream;
                video.play();
            });
    }

    function drawCanvas() {
                context.drawImage(video, 0, 0, 600, 450);
                sendMessage(canvas.toDataURL('image/png'));
            }

    document.getElementById("start_pred").addEventListener("click", function () {
                drawCanvas();
            });

    function sendMessage(message) {
                socket.send(message);
            }
            socket.onmessage = function (e) {
                image.onload = function () {
                    context.drawImage(image, 0, 0, 600, 450);
                };
                image.src = e.data;
                //console.log(image.src)
                drawCanvas();
            };
});


