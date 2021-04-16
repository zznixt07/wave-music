

// import {Rythm} from './rythm.js'

// const rythm = new Rythm()
// rythm.setMusic('user/audio/1.mp3')
// rythm.start()

const ap = new APlayer({
    container: document.getElementById('3rd-p-player'),
    listFolded: false,
    listMaxHeight: 90,
    audio: [
        {
            name: 'Ongoing Theme',
            artist: '20syl',
            url: '/static/user/audio/1.mp3',
        },
    ],
});

document.querySelector('.aplayer .aplayer-info').insertAdjacentHTML(
    'afterbegin',
    `<div class="controls-btns">
        <button class="prev-track ri-skip-back-fill"></button>
        <button class="play-or-pause-track ri-play-circle-fill"></button>
        <button class="next-track ri-skip-forward-fill"></button>
    </div>`
)


const playPauseBtn = document.querySelector('.play-or-pause-track')
let paused = true
playPauseBtn.addEventListener('click', function () {
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
    playPauseBtn.classList.remove('ri-play-circle-fill')
    playPauseBtn.classList.add('ri-pause-circle-fill')
})

ap.on('pause', function () {
    playPauseBtn.classList.remove('ri-pause-circle-fill')
    playPauseBtn.classList.add('ri-play-circle-fill')  
})


const btn = document.getElementById('button')
btn.addEventListener('click', function () {
    ap.list.add([
        {
            name: 'walking on the moon',
            artist: 'Computer Glitch',
            url: '/static/user/audio/walking.webm',
        },
    ]);
})