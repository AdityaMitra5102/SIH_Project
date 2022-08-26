const uploadFile = document.getElementById("upload");
const encrypt = document.getElementById('encrypt');
const hidden = document.getElementById('hidden');
const compressedArea = document.getElementsByClassName('compressed-area');

function upload_file(file) {
    const file_length = (file.size) / 1000;
    const duration = file_length / 1.96;
    const percent = duration /100;
    // progressArea.stop().css("width", 0).animate({
    //     width: 100
    //   }, {
    //     duration: duration,
    //     progress: function(promise, progress, ms) {
    //       $(this).text(Math.round(progress * 100) + '%');
    //     }
    //   });
    var i = 1;
    var progress = document.getElementsByClassName('progress');
    // progress.setAttribute('id', 'play-animation');
    progress.style.animation = `progress-animation ${percent}`;
    // var interval = setInterval(function () {
    //     i++;
    //     progress.style.width = `${i}%`;
    //     // i++;
    //     // progressArea.css("width", i + "px");
    //     if(i >= 100){
    //         alert("done");
    //         clearInterval(interval);
    //     }
    // }, 10)
    console.log(duration);
}

if (encrypt.checked){
        hidden.style.display = "block";
    } else {
        hidden.style.display = "none";
}

encrypt.addEventListener('change', (e) => {
    if (e.target.checked){
        hidden.style.display = "block";
    } else {
        hidden.style.display = "none";
    }
  });
