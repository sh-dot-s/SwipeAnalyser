// define how elements are taken from the DOM

export function getElementsByClass (query) {
    return document.getElementsByClass(query);
}

export function getElementsByTagName (query) {
    return document.getElementsBYTagName(query);
}

export function querySelectorAll (query, item = document) {
    return item.querySelectorAll(query);
}

export function isValidAnimationContainer (item) {
    if(item.querySelectorAll('[data-animation]').length > 0) {
        return true;
    } else {
        console.error("Invalid animation item. The element or its children is missing a data-animation attribute: ", item);
        return false;
    }
}

export function animate(element) {
    $(element).addClass('animated ' + $(element).attr('data-animation-type'));
}

export function timedAnimate (element, timeout) {
    setTimeout(function () {
        animate(element);
    }, timeout);
}

export function getMiddlePos (element) {
	return $(element).offset().top + ($(element).height() / 2);
}

export function tryParseInt(value) {
    if (value !== null && typeof value !== 'undefined') {
        if (value.length > 0) {
            if (!isNaN(value)) {
                return parseInt(value);
            }
        }
    }
    return null;
}

export function tryParseInt(value, def) {
    if (value !== null && typeof value !== 'undefined') {
        if (value.length > 0) {
            if (!isNaN(value)) {
                return parseInt(value);
            }
        }
    }
    return def;
}
