
const closeForm = () => {
    playlistForm.classList.add('display-none')
}

let SELECTED_SONG;
// const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value
const playlistForm = document.querySelector('.playlist-add')

// show list of playlist to add to after clicking add to playlist button
const addToPlaylistBtns = document.querySelectorAll('.playlist-this')
addToPlaylistBtns.forEach((playlistBtn) => {
    playlistBtn.addEventListener('click', () => {
        playlistForm.classList.remove('display-none')
        SELECTED_SONG = playlistBtn.parentElement.dataset.trackId
    })
})

// close the dialog showing a list of playlist.
const closeListPlaylistsBtn = document.querySelector('.close-btn')
closeListPlaylistsBtn.addEventListener('click', closeForm)
playlistForm.addEventListener('click', closeForm)

// add a song to playlist after choosing the playlist
const playlistElems = document.querySelectorAll('.add-to-playlist p')
playlistElems.forEach((pl) => {
    pl.addEventListener('click', () => {
        const playlistId = pl.dataset.playlistId
        fetch('/playlist/'+playlistId+'/' , {
            method: 'POST',
            body: JSON.stringify({track_id: SELECTED_SONG}),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
        }).then(resp => resp.json())
            .then(data => console.log(data))
                .catch(err => console.log(err))
    })
})

// toggle heart state and store track in favourites
const heartAnchors = document.querySelectorAll('.heart')
heartAnchors.forEach((heartAnchor) => {
    heartAnchor.addEventListener('click', () => {
        let method = 'POST'
        if (toggleClass(heartAnchor, 'ri-heart-3-fill', 'ri-heart-3-line') === 'ri-heart-3-line') {
            method = 'DELETE'
        }
        fetch('/playlist/favourites/', {
            method: method,
            body: JSON.stringify({
                track_id: heartAnchor.parentElement.dataset.trackId
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
        }).then(resp => resp.json())
            .then(data => console.log(data))
                .catch(err => console.log(err))
    })
})

function playOne(trackId, clearQueue) {
    window.parent.postMessage({
        type: 'playTrack',
        track: {id: trackId},
        clearQueue: clearQueue,
    }, 'http://127.0.0.1:8000')
}

// play this track
const playBtns = document.querySelectorAll('.play-this')
playBtns.forEach((playBtn) => playBtn.addEventListener('click', () => {
    const trackId = parseInt(playBtn.parentElement.parentElement.dataset.trackId, 10)
    playOne(trackId, true)
}))

// queue this track
const queueBtns = document.querySelectorAll('.queue-this')
queueBtns.forEach((qBtn) => qBtn.addEventListener('click', () => {
    const trackId = parseInt(qBtn.parentElement.dataset.trackId, 10)
    playOne(trackId, false)
}))

// play all songs in the playlist
const playAll = document.querySelector('.play-playlist')
playAll.addEventListener('click', () => {
    const trackIds = Array.from(document.querySelectorAll('[data-track-id]'))
                            .map((t) => t.dataset.trackId)
    const tracks = [];
    trackIds.forEach((id) => {
        tracks.push({'id': id})
    })
    window.parent.postMessage({
        type: 'queueTracks',
        tracks: tracks,
        clearQueue: true,
    }, 'http://127.0.0.1:8000')
})