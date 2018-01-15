var events = require('./events.js');
var functions = require('./functions.js')

export class AnimationContainer {
    constructor (container) {
        // store the element with the data annotation "data-animation-condition"
        this.element = container;
        this.setProperties();
        this.setAnimation();
        this.setEvent();
    }


    setProperties () {
        // items are nested elements with the data annotation "data-animation"
        // these are the elements that actually animates
        this.items = [];
        this.nextItem = 0;

        // for every animatable element, create the animation sequence
        var element = $(this.element);
        $(element).find('[data-animation]').each( (i, e) => {
            // animations and timeouts should be parallel arrays
            // timeouts are values in milliseconds that tell when next animation
            //      should play
            var animations = $(e).attr('data-animation').split(",");
            var timeouts = $(e).attr('data-animation-timeouts') || "";
            var delay = $(e).attr('data-animation-delay') || $(this.element).attr('data-animation-interval') || 0;

            // create an item object and store the element for quick access
            var item = {
                delay,
                index: i,
                element: e,
                cue: 0,
                nextAnimation: 0,
                animations,
                timeouts: [],
            };

            item.checkCue = () => {
                if(item.cue === item.nextAnimation) {
                    if(item.index + 1 === this.nextItem) {
                        this.animateNext();
                    }
                }
            }

            // replace the previous animation class with the next one
            item.playNextAnimation = function () {
                $(item.element).removeClass(item.animations[item.nextAnimation++]);
                // this checks if animation is supposed to be infinite
                // if so, set the next animation to be the first animation
                if(item.nextAnimation >= item.animations.length && $(item.element).attr('data-animation-infinite') !== 'undefined') {
                    item.nextAnimation = 0;
                }

                $(item.element).addClass(item.animations[item.nextAnimation]);
            }

            // once animation ends, check when to trigger next animation
            // also figure out when to trigger the next animatable item
            $(e).on('animationend webkitAnimationEnd oAnimationEnd', () => {
                // TODO: check if next item in AnimationItem should be triggered
                //      before or after next animation
                item.checkCue();

                // TODO: this should set up a delay based on the timeouts array
                setTimeout(function () {
                    item.playNextAnimation(); //this should be timed
                }, item.timeouts[item.nextAnimation]);
            });

            // create the array of timeouts, array of 0s if not available
            if(typeof timeouts === 'string') {
                timeouts = timeouts.split(",");
                for(var j = 0;  j < animations.length; j ++) {
                    item.timeouts.push(functions.tryParseInt(timeouts[j], 0));
                }
            }

            // cue is defaulted to before the first animation
            var cue = functions.tryParseInt($(e).attr('data-continue-on'), null);

            if(cue !== null) {
                if(cue > items.animations.length || cue < 0) {
                    console.error("Invalid cue value", item.element);
                }
            }

            // this is the initializes the chain of animations within an item
            item.animate = function()  {
                setTimeout( function () {
                    item.checkCue();
                    $(item.element).addClass(item.animations[item.nextAnimation] + " animated");
                }, item.delay);
            }

            this.items.push(item);

        });

        this.condition = element.attr('data-animation-condition');

        this.animateNext = () => {
            if(this.nextItem < this.items.length) {
                this.items[this.nextItem++].animate();
            }
        }
    }

    setAnimation () {
        this.animate = () => {
            this.animateNext();
        }
    }


    setEvent () {
        var type = this.element.getAttribute("data-animation-condition");

        switch (type) {
            case 'seen':
                events.addSeenItem(this);
                break;
            default:
                console.error("Condition data attribute value is not supported. Check documentation for accepted values.", item);
        }
    }
}
