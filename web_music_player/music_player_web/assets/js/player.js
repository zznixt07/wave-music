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
    ]
});

const btn = document.getElementById('button')
btn.addEventListener('click', function () {
    ap.list.add([
        {
            name: 'walking on the moon',
            artist: 'Computer Glitch',
            url: './assets/audio/walking.webm',
        },
    ]);

})