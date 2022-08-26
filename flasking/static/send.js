const uploadFile = document.getElementById("upload");
const encrypt = document.getElementById('encrypt');
const hidden = document.getElementById('hidden');
const compressedArea = document.getElementsByClassName('compressed-area');

// function upload_file(file) {
//     const file_length = (file.size) / 1000;
//     const duration = file_length / 1.96;
//     var i = 1;
//     var progress = document.getElementsByClassName('progress');
//     // progress.setAttribute('id', 'play-animation');
//     progress.style.animation = `progress-animation ${duration/100}`;
//     console.log(duration);
// }

button.onclick = (e) => {
    e.preventDefault();

    const file = document.getElementById('myFile');
// const userFile = file.files[0];
    input.click();
    options.style.display = 'block';
    upload_file(file);
}


encrypt.addEventListener('change', (e) => {
    if (e.target.checked){
        hidden.style.display = "block";
    } else {
        hidden.style.display = "none";
    }
});

compress.addEventListener('change', (e) => {

    const file = document.getElementById('myFile');
    const userFile = file.files[0];
    
    if (e.target.checked){
        hideOnCompress.style.display = "block";
        upload_file(userFile);
    } else {
        hideOnCompress.style.display = "none";
    }
})

function upload_file(file) {
    const file_length = (file.size) / 1000;
    const duration = file_length / 1.96;
    const time = duration/100;
    let progress = document.querySelector('.progress');
    let progressVal = 0;
    const fakeUploadPerc = [0, 10, 25, 40, 45, 60, 70, 90, 100];

    let interval = setInterval(() => {
        progress.style.width = `${fakeUploadPerc[progressVal]}%`;
        progressVal++;
        if(progressVal === duration){
            clearInterval(interval)
        }
    }, 1000)

console.log(progress);

    console.log(time);
}
// const uploadFile = document.getElementById("upload");
// const encrypt = document.getElementById('encrypt');
// const compress = document.getElementById('compress');
// const hidden = document.getElementById('hidden');
// const password = document.getElementById('password');
// const options = document.getElementById('options');
// const compressedArea = document.getElementsByClassName('compressed-area');
// const hideOnCompress = document.getElementById('on_compress');


// const input = document.getElementById('myFile');

// const button = document.getElementById('input_btn');


// uploadFile.addEventListener("submit", (event) => {
//     event.preventDefault();

// //     const file = document.getElementById('myFile');
// // const userFile = file.files[0];

// //     const formData = new FormData();
// //     formData.append('user-file', userFile);
// //     formData.append('encryt-password', password.value);

// //     // console.log(password.value);


// //     fetch('https://httpbin.org/post', {
// //         method: 'POST',
// //         body: formData
// //     })
// //     .then(resp => resp.json())
// //     .then(data => console.log(data))
// //     .catch(err => console.log(err))

// });
