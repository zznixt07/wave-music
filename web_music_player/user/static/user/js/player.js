

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


const btn = document.getElementById('button')
btn.addEventListener('click', function () {
    player.list.add([
        {
            name: 'walking on the moon',
            artist: 'Computer Glitch',
            url: '/static/user/audio/walking.webm',
        },
    ]);
})

async function getTrack(id) {
    return (
        await fetch('track/getTrack/' + id, {
            method: 'GET',
            }).then(resp => resp.json())
                .then(data => data)
                    .catch(err => console.log(err))
    )
}

function playTrack(track) {
    player = new APlayer({
        container: container,
        listFolded: false,
        listMaxHeight: 90,
        audio: [
            {
                name: track.title,
                artist: Object.values(track.artists[0])[0],
                url: 'media/' + track.audio_url,
                cover: 'media/' + track.image_url,
            },
        ],
    })
    player.play()
}

// listen messages from iframe
window.addEventListener('message', async (event) => {
    if (event.origin !== 'http://127.0.0.1:8000') return
    const data = event.data
    if (data.type === 'ACK') return

    console.log("data from iframe :", data)
    event.source.postMessage({
        type: 'ACK',
        recieved: data,
    }, event.origin)

    if (data.type === 'playTrack') {
        const trackDetails = await getTrack(data.track.id)
        console.log(trackDetails)
        playTrack(trackDetails)
    }
})