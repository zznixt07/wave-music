function randomInt(min, max) {
    // [min-max)
    return Math.floor(Math.random() * (max - min)) + min
}

// returns the class added
function toggleClass(elem, cls1, cls2) {
    classes = elem.classList
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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}