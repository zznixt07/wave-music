// import {Rythm} from './rythm.js'

// const rythm = new Rythm()
// rythm.setMusic('./assets/audio/1.mp3')
// rythm.start()

const ap = new APlayer({
    container: document.getElementById('3rd-p-player'),
    listFolded: false,
    listMaxHeight: 90,
    audio: [
        {
            name: 'Ongoing Theme',
            artist: '20syl',
            url: './assets/audio/1.mp3',
        },
    ],
});


const audioElem = document.querySelector('audio')
const playPauseBtn = document.querySelector('.play-or-pause-track')
let paused = true
playPauseBtn.addEventListener('click', function () {
    // audioElem.play()
    if (paused) {
        ap.play()
        paused = false
    }
    else {
        ap.pause()
        paused = true
    }

})

ap.on('play', function () {
    playPauseBtn.textContent = '||'
})

ap.on('pause', function () {
    playPauseBtn.textContent = '|>'
})

document.querySelector('.aplayer .aplayer-music').insertAdjacentHTML(
    'beforeend',
    `<div class="controls-btns">
        <button class="prev-track">Prev</button>
        <button class="play-or-pause-track">|></button>
        <button class="next-track">Next</button>
    </div>`
)


// const btn = document.getElementById('button')
// btn.addEventListener('click', function () {
//     ap.list.add([
//         {
//             name: 'walking on the moon',
//             artist: 'Computer Glitch',
//             url: './assets/audio/walking.webm',
//         },
//     ]);
// })