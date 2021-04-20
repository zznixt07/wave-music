import { spectrum } from './oscillator.js'

function randomInt(min, max) {
    // [min-max)
    return Math.floor(Math.random() * (max - min)) + min
}

// returns the class added
function toggleClass(elem, cls1, cls2) {
    const classes = elem.classList
    if (Array.from(classes).indexOf(cls1) !== -1) {
        classes.remove(cls1)
        classes.add(cls2)
        return cls2
    }
    // below:: using if is different than using else
    else {
        classes.remove(cls2)
        classes.add(cls1)
        return cls1
    }
}

// import {Rythm} from './rythm.js'

// const rythm = new Rythm()
// rythm.setMusic('user/audio/1.mp3')
// rythm.start()

const container = document.getElementById('3rd-p-player')
let player = new APlayer({
    container: container,
    listFolded: false,
    listMaxHeight: 90,
    audio: [
        {
            name: 'Ongoing Theme',
            artist: '20syl',
            url: '/static/user/audio/1.mp3',
        },
    ],
    theme: '#445366',
});

document.querySelector('.aplayer .aplayer-info').insertAdjacentHTML(
    'afterbegin',
    `<div class="controls-btns">
        <button class="prev-track ri-skip-back-fill"></button>
        <button class="play-or-pause-track ri-play-circle-fill"></button>
        <button class="next-track ri-skip-forward-fill"></button>
        <button style="font-size: 120%;" class="spectrum ri-magic-line"></button>
    </div>`
)

const magic = document.querySelector('.spectrum')
const canvas = document.querySelector('canvas')
let visualized = false
magic.addEventListener('click', () => {
    const added = toggleClass(magic, 'ri-magic-line', 'ri-magic-fill')
    
    if (added === 'ri-magic-fill') {
        canvas.style.display = 'block'
        if (visualized) return
        visualized = true;
        spectrum(0.8, player.audio)
    }
    else {
        canvas.style.display = 'none'
    }
})

document.querySelector('.prev-track').addEventListener('click', () => player.skipBack())
document.querySelector('.next-track').addEventListener('click', () => player.skipForward())
const playPauseBtn = document.querySelector('.play-or-pause-track')
let paused = true
playPauseBtn.addEventListener('click', function () {
    player.toggle()
})

player.on('play', function () {
    playPauseBtn.classList.remove('ri-play-circle-fill')
    playPauseBtn.classList.add('ri-pause-circle-fill')
})

player.on('pause', function () {
    playPauseBtn.classList.remove('ri-pause-circle-fill')
    playPauseBtn.classList.add('ri-play-circle-fill')  
})


async function getTrack(id) {
    return (
        await fetch('/track/getTrack/' + id, {
            method: 'GET',
            }).then(resp => resp.json())
                .then(data => data)
                    .catch(err => console.log(err))
    )
}

function addToQueue(tracks) {
    tracks.forEach((track) => {
        player.list.add([{
            name: track.title,
            artist: Object.values(track.artists[0])[0],
            url: 'media/' + track.audio_url,
            cover: 'media/' + track.image_url,
        }])
    })
    player.play()
}

function playTrack(track) {
    
    player.list.add([{
        name: track.title,
        artist: Object.values(track.artists[0])[0],
        url: 'media/' + track.audio_url,
        cover: 'media/' + track.image_url,
    }])

    player.play()
}

// listen messages from iframe
window.addEventListener('message', async (event) => {
    if (event.origin !== 'http://127.0.0.1:8000') return
    const data = event.data
    if (data.type === 'ACK') return

    // event.source.postMessage({
    //     type: 'ACK',
    //     recieved: data,
    // }, event.origin)
    console.log("data from iframe :", data)

    if (data.clearQueue) player.list.clear()
    if (data.type === 'playTrack') {
        const trackDetails = await getTrack(data.track.id)
        playTrack(trackDetails)
    }
    else if (data.type == 'queueTracks') {
        const tracks = []
        for (const track of data.tracks) {
            if (track.hasOwnProperty('id')) {
                tracks.push(await getTrack(track.id))
            }
        }
        addToQueue(tracks)
    }
})
