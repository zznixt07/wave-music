
// given playlistid, artistid, albumid; fetch and queue the tracks
function request(url, id) {            
    fetch(url + id + '/', {
        method: 'GET',
    }).then(resp => resp.json())
        .then(trackIds => {
            const tracks = []
            trackIds.forEach((id) => {
                tracks.push({'id': id})
            })
            window.parent.postMessage({
                type: 'queueTracks',
                tracks: tracks,
                clearQueue: true,
            }, 'http://127.0.0.1:8000')
        })
    
}

// play the playlist, album or artists tracks
const playPlaylistBtns = document.querySelectorAll('.hover-play-card')
playPlaylistBtns.forEach((btn) => {
    btn.addEventListener('click', (event) => {
        event.preventDefault()
        const playlistId = btn.dataset.playlistId
        const artistId = btn.dataset.artistId
        const albumId = btn.dataset.albumId
        if (playlistId) {
            request('/playlist/getTracks/', playlistId)
        }
        else if (artistId) {
            request('/artist/getTracks/', artistId)
        }
        else if (albumId) {
            request('/album/getTracks/', albumId)
        }
    })
})
