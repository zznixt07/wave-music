export function spectrum(degreeTheta, audioElem) {



function random(min, max) {
    // [min-max)
    return (Math.random() * (max - min)) + min
}

function randomInt(min, max) {
    // [min-max)
    return Math.floor(Math.random() * (max - min)) + min
}

function degToRad(degrees) {
    return degrees * Math.PI / 180
}

function radToDeg(rad) {
    return rad * 180 / Math.PI
}

function sine(deg) {
    return Math.sin(degToRad(deg))
}

function cosine(deg) {
    return Math.cos(degToRad(deg))
}

function tangent(deg) {
    return Math.tan(degToRad(deg))
}

function sum(arr) {
    // reduce takes func and an initial value
    return arr.reduce((total, currElem) => total + currElem, 0)
}

function max(arr) {
    return arr.reduce((maximum, currElem) => Math.max(maximum, currElem))
}

function min(arr) {
    return arr.reduce((maximum, currElem) => Math.min(maximum, currElem))
}

function sliceIntoEqualParts(arr, n) {
    // 'ensures all section has same no. of item. but strips item.'
    const parts = []
    const slice_point = Math.floor(arr.length / n)
    for (let i = 0; i < n; i++) {
        parts.push(arr.slice(slice_point*i,slice_point*(i+1)))
    }

    return parts
}

function getCurrVol() {
    analyser.getByteTimeDomainData(times)
    let rms = 0
    for (let i = 0; i < times.length; i++) {
        rms += times[i] ** 2
    }
    return Math.abs(Math.sqrt(rms / times.length))
}


class Matter {

    constructor(x, y, velX, velY, exists) {
        this.x = x
        this.y = y
        this.velX = velX
        this.velY = velY
        this.exists = exists
    }
}

class ZDot extends Matter {

    constructor(x, y, velX, velY, radius, color, transparency, exists) {
        super(x, y, velX, velY, exists)
        this.radius = radius
        this.initialRadius = radius
        this.color = color
        this.transperency = transparency
        // Math.atan() can only output [-90, +90] but Math.atan2() can do [-180, +180]
        this.angle = radToDeg(Math.atan2((this.y - height / 2), (this.x - width / 2)))
        this.velX = this.velX * cosine(this.angle)
        this.velY = this.velY * sine(this.angle)
    }

    draw() {
        if (this.exists) {
            canvasCtx.beginPath()
            canvasCtx.fillStyle = this.color
            canvasCtx.arc(this.x, this.y, this.radius, 0, Math.PI * 2)
            canvasCtx.fill()
            return true
        }
        return false
    }

    update() {
        if (this.x < 0 || this.y < 0 || this.x > width || this.y > height) {
            this.exists = false
        }
        this.x += this.velX
        this.y += this.velY
        const totalSize = 0.5 * Math.abs(this.x - width / 2) + 0.5 * Math.abs(this.y - height / 2)
        this.radius = tangent(0.3) * totalSize + this.initialRadius
    }
}

function animate(ts) {
    
    canvasCtx.fillRect(0, 0, width, height)
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    // canvasCtx.drawImage(IMAGEOBJ, 0, 0, 1920, 1080)

    analyser.getFloatFrequencyData(frequencies)
    
    // the main circle in center holding the spectrum
    canvasCtx.lineWidth = 2
    canvasCtx.strokeStyle = 'white'
    canvasCtx.beginPath()
    canvasCtx.arc(h, k, circleRadius, 0, Math.PI * 2)
    canvasCtx.stroke()
    let musicPaused = true
    // const gap = Math.floor(frequencies.length / num)
    for (let i = 0; i < num; i++) {
        // : use with higher angles
        // const index = Math.floor((i * gap) % frequencies.length)
        // minorAxisLen = (frequencies[index] + 160)
        minorAxisLen = (frequencies[i] + 160)
        degreeTheta += originalTheta
        posX = circleRadius * cosine(degreeTheta) + h
        posY = circleRadius * sine(degreeTheta) + k

        if (minorAxisLen >= 0) {
            if (musicPaused) musicPaused = false
            canvasCtx.beginPath()
            // canvasCtx.strokeStyle = `rgb(${255 - minorAxisLen}, 122, 255)`
            // // ellipse is rotated by 90 degrees.
            // canvasCtx.ellipse(posX, posY, majorAxisLen/2, minorAxisLen/2, degToRad(degreeTheta+90), 3.13, 6.3)
            // canvasCtx.stroke()

            canvasCtx.translate(posX, posY)
            canvasCtx.rotate(degToRad(degreeTheta+40))
            canvasCtx.translate(-(posX), -(posY))

            canvasCtx.fillStyle = `rgb(${255 - minorAxisLen}, 122, 255)`
            canvasCtx.fillRect(posX, posY, minorAxisLen/2, majorAxisLen)
            canvasCtx.setTransform(1, 0, 0, 1, 0, 0) // Reset the angle too.
        }
    }

    if (!musicPaused) {
        for (let i = 0; i < dots.length; i++) {
            const dot = dots[i]
            if (!dot.exists) {
                dots[i] = createArbitraryMatter()
            }
            dot.draw()
            dot.update()
        }
    }

    REQUESTID = window.requestAnimationFrame(animate)
}

function createArbitraryMatter() {
    // radius = randomInt(0, 1.01) ? random(2.0, 4.0) : random(0.01, 2.0)
    posX = random(width / 2 - birthRad, width / 2 + birthRad)
    posY = random(height / 2 - birthRad, height / 2 + birthRad)
    radius = random(0.4, 1)
    velX = random(1, 3)
    velY = random(1, 3)
    // velX = velY = 5
    color = '#ffffff'
    return new ZDot(posX, posY, velX, velY, radius, color, 1, true)
}

function audioInit() {
    console.log('audio comps.. initializing')
    audioElem.removeEventListener('play', audioInit)

    audioCtx = new AudioContext()
    audioSourceNode = audioCtx.createMediaElementSource(audioElem);
    gainNode = audioCtx.createGain()
    analyser = audioCtx.createAnalyser()
    analyser.fftSize = 2048
    bufferLength = analyser.frequencyBinCount
    frequencies = new Float32Array(bufferLength)
    times = new Uint8Array(analyser.fftSize)

    //setup audio node network
    audioSourceNode.connect(analyser)
                    .connect(gainNode)
                    .connect(audioCtx.destination)
    animate()
}


let audioCtx, audioSourceNode, gainNode, analyser, frequencies, times, bufferLength
// let currCircleRad = 150
let REQUESTID

// setup canvas
const canvas = document.querySelector('canvas')
const canvasCtx = canvas.getContext('2d')
const width = canvas.width = window.innerWidth
const height = canvas.height = window.innerHeight

// let audioElem
// const IMAGEOBJ = new Image()
// IMAGEOBJ.src = "./assets/back.jpg"

// circle visuals
let circleRadius = 120
// let degreeTheta = 0.8
const originalTheta = degreeTheta
const h = window.innerWidth / 2
const k = window.innerHeight / 2
// const majorAxisLen = (circleRadius * sine(degreeTheta)) / sine(90 - degreeTheta)
const majorAxisLen = Math.sqrt((2 * circleRadius ** 2) * (1 - cosine(degreeTheta)))

// const num = (2 * Math.PI * circleRadius) / majorAxisLen
const num = 360 / degreeTheta
let minorAxisLen, posX, posY

let dots = []
const TAILOPACITY = 0.2
let velX, velY, radius, color
const NUMOFDOTS = 200
const birthRad = 3

for (let i = 0; i < NUMOFDOTS; i++) {
    dots.push(createArbitraryMatter())
}

audioInit()

}

