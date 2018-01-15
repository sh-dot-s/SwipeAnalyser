/*
    TODO:
        * Replace jQuery dependent functions
        * Add the option to reset animations on specified condition
*/

var conditions = require('./lib/conditions.js');
var functions = require('./lib/functions.js');
var events = require('./lib/events.js');
var { AnimationContainer } = require('./lib/classes.js');

var animationContainers = [];

// get all valid objects with data-animation-condition attribute, store them in an array as Animation Item
for (let element of functions.querySelectorAll('[data-animation-condition]')) {
    if (functions.isValidAnimationContainer(element)) {
        animationContainers.push(new AnimationContainer(element));
    }
}

events.checkAllItems();

//
// var animateJs = {
//     // not needed yet
// }
//
//
// module.exports = animateJs;
