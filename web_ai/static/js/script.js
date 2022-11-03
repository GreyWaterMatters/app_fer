let app = {
  stopCamera: (container) => {
    for (const track of container.srcObject.getTracks()) {
      track.stop();
    }
    console.log("stopping track")
    container.srcObject = null;
  },
  init: () => {
    const video = document.querySelector('.video-streamer');
    console.log(video.srcObject)
    console.log("in init")
    app.stopCamera(video);
  },

};

// Lorsque la page est totalement chargée, on lance la fonction app.init
document.addEventListener('DOMContentLoaded', app.init);

