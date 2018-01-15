(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define("animateJs", [], factory);
	else if(typeof exports === 'object')
		exports["animateJs"] = factory();
	else
		root["animateJs"] = factory();
})(this, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;
/******/
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	/*
	    TODO:
	        * Replace jQuery dependent functions
	        * Add the option to reset animations on specified condition
	*/
	
	var conditions = __webpack_require__(1);
	var functions = __webpack_require__(2);
	var events = __webpack_require__(3);
	
	var _require = __webpack_require__(4);
	
	var AnimationContainer = _require.AnimationContainer;
	
	
	var animationContainers = [];
	
	// get all valid objects with data-animation-condition attribute, store them in an array as Animation Item
	var _iteratorNormalCompletion = true;
	var _didIteratorError = false;
	var _iteratorError = undefined;
	
	try {
	    for (var _iterator = functions.querySelectorAll('[data-animation-condition]')[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
	        var element = _step.value;
	
	        if (functions.isValidAnimationContainer(element)) {
	            animationContainers.push(new AnimationContainer(element));
	        }
	    }
	} catch (err) {
	    _didIteratorError = true;
	    _iteratorError = err;
	} finally {
	    try {
	        if (!_iteratorNormalCompletion && _iterator.return) {
	            _iterator.return();
	        }
	    } finally {
	        if (_didIteratorError) {
	            throw _iteratorError;
	        }
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

/***/ },
/* 1 */
/***/ function(module, exports) {

	"use strict";
	
	module.exports = {};

/***/ },
/* 2 */
/***/ function(module, exports) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	exports.getElementsByClass = getElementsByClass;
	exports.getElementsByTagName = getElementsByTagName;
	exports.querySelectorAll = querySelectorAll;
	exports.isValidAnimationContainer = isValidAnimationContainer;
	exports.animate = animate;
	exports.timedAnimate = timedAnimate;
	exports.getMiddlePos = getMiddlePos;
	exports.tryParseInt = tryParseInt;
	exports.tryParseInt = tryParseInt;
	// define how elements are taken from the DOM
	
	function getElementsByClass(query) {
	    return document.getElementsByClass(query);
	}
	
	function getElementsByTagName(query) {
	    return document.getElementsBYTagName(query);
	}
	
	function querySelectorAll(query) {
	    var item = arguments.length <= 1 || arguments[1] === undefined ? document : arguments[1];
	
	    return item.querySelectorAll(query);
	}
	
	function isValidAnimationContainer(item) {
	    if (item.querySelectorAll('[data-animation]').length > 0) {
	        return true;
	    } else {
	        console.error("Invalid animation item. The element or its children is missing a data-animation attribute: ", item);
	        return false;
	    }
	}
	
	function animate(element) {
	    $(element).addClass('animated ' + $(element).attr('data-animation-type'));
	}
	
	function timedAnimate(element, timeout) {
	    setTimeout(function () {
	        animate(element);
	    }, timeout);
	}
	
	function getMiddlePos(element) {
	    return $(element).offset().top + $(element).height() / 2;
	}
	
	function tryParseInt(value) {
	    if (value !== null && typeof value !== 'undefined') {
	        if (value.length > 0) {
	            if (!isNaN(value)) {
	                return parseInt(value);
	            }
	        }
	    }
	    return null;
	}
	
	function tryParseInt(value, def) {
	    if (value !== null && typeof value !== 'undefined') {
	        if (value.length > 0) {
	            if (!isNaN(value)) {
	                return parseInt(value);
	            }
	        }
	    }
	    return def;
	}

/***/ },
/* 3 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
		value: true
	});
	exports.addSeenItem = addSeenItem;
	exports.addItem = addItem;
	exports.checkAllItems = checkAllItems;
	var functions = __webpack_require__(2);
	// data-animation-type="seen" ==================================================
	var seenItems = [];
	
	// check if middle pos of any item is in browser
	function checkSeen() {
		var _iteratorNormalCompletion = true;
		var _didIteratorError = false;
		var _iteratorError = undefined;
	
		try {
	
			for (var _iterator = seenItems[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
				var item = _step.value;
	
				var viewTop = $(window).scrollTop();
				var viewBottom = viewTop + $(window).height();
	
				if (item.middlePos <= viewBottom && item.middlePos >= viewTop) {
					item.animate();
					seenItems.splice(seenItems.indexOf(item), 1);
	
					if (seenItems.length == 0) {
						$(window).off('scroll', this); // not properly unbinding scroll event
					}
				}
			}
		} catch (err) {
			_didIteratorError = true;
			_iteratorError = err;
		} finally {
			try {
				if (!_iteratorNormalCompletion && _iterator.return) {
					_iterator.return();
				}
			} finally {
				if (_didIteratorError) {
					throw _iteratorError;
				}
			}
		}
	}
	
	// bind check seen items to window scroll upon adding first item
	function addSeenItem(item) {
		if (seenItems.length == 0) {
			$(window).on('scroll', checkSeen);
		}
		item.middlePos = functions.getMiddlePos(item.element);
		seenItems.push(item);
	}
	//==============================================================================
	
	function addItem(element) {}
	
	function checkAllItems() {
		checkSeen();
	}
	
	// on some cases, event conditions may change
	// check if window resizes, then recalculate middlePos in seenItems

/***/ },
/* 4 */
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();
	
	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
	
	var events = __webpack_require__(3);
	var functions = __webpack_require__(2);
	
	var AnimationContainer = exports.AnimationContainer = function () {
	    function AnimationContainer(container) {
	        _classCallCheck(this, AnimationContainer);
	
	        // store the element with the data annotation "data-animation-condition"
	        this.element = container;
	        this.setProperties();
	        this.setAnimation();
	        this.setEvent();
	    }
	
	    _createClass(AnimationContainer, [{
	        key: 'setProperties',
	        value: function setProperties() {
	            var _this = this;
	
	            // items are nested elements with the data annotation "data-animation"
	            // these are the elements that actually animates
	            this.items = [];
	            this.nextItem = 0;
	
	            // for every animatable element, create the animation sequence
	            var element = $(this.element);
	            $(element).find('[data-animation]').each(function (i, e) {
	                // animations and timeouts should be parallel arrays
	                // timeouts are values in milliseconds that tell when next animation
	                //      should play
	                var animations = $(e).attr('data-animation').split(",");
	                var timeouts = $(e).attr('data-animation-timeouts') || "";
	                var delay = $(e).attr('data-animation-delay') || $(_this.element).attr('data-animation-interval') || 0;
	
	                // create an item object and store the element for quick access
	                var item = {
	                    delay: delay,
	                    index: i,
	                    element: e,
	                    cue: 0,
	                    nextAnimation: 0,
	                    animations: animations,
	                    timeouts: []
	                };
	
	                item.checkCue = function () {
	                    if (item.cue === item.nextAnimation) {
	                        if (item.index + 1 === _this.nextItem) {
	                            _this.animateNext();
	                        }
	                    }
	                };
	
	                // replace the previous animation class with the next one
	                item.playNextAnimation = function () {
	                    $(item.element).removeClass(item.animations[item.nextAnimation++]);
	                    // this checks if animation is supposed to be infinite
	                    // if so, set the next animation to be the first animation
	                    if (item.nextAnimation >= item.animations.length && $(item.element).attr('data-animation-infinite') !== 'undefined') {
	                        item.nextAnimation = 0;
	                    }
	
	                    $(item.element).addClass(item.animations[item.nextAnimation]);
	                };
	
	                // once animation ends, check when to trigger next animation
	                // also figure out when to trigger the next animatable item
	                $(e).on('animationend webkitAnimationEnd oAnimationEnd', function () {
	                    // TODO: check if next item in AnimationItem should be triggered
	                    //      before or after next animation
	                    item.checkCue();
	
	                    // TODO: this should set up a delay based on the timeouts array
	                    setTimeout(function () {
	                        item.playNextAnimation(); //this should be timed
	                    }, item.timeouts[item.nextAnimation]);
	                });
	
	                // create the array of timeouts, array of 0s if not available
	                if (typeof timeouts === 'string') {
	                    timeouts = timeouts.split(",");
	                    for (var j = 0; j < animations.length; j++) {
	                        item.timeouts.push(functions.tryParseInt(timeouts[j], 0));
	                    }
	                }
	
	                // cue is defaulted to before the first animation
	                var cue = functions.tryParseInt($(e).attr('data-continue-on'), null);
	
	                if (cue !== null) {
	                    if (cue > items.animations.length || cue < 0) {
	                        console.error("Invalid cue value", item.element);
	                    }
	                }
	
	                // this is the initializes the chain of animations within an item
	                item.animate = function () {
	                    setTimeout(function () {
	                        item.checkCue();
	                        $(item.element).addClass(item.animations[item.nextAnimation] + " animated");
	                    }, item.delay);
	                };
	
	                _this.items.push(item);
	            });
	
	            this.condition = element.attr('data-animation-condition');
	
	            this.animateNext = function () {
	                if (_this.nextItem < _this.items.length) {
	                    _this.items[_this.nextItem++].animate();
	                }
	            };
	        }
	    }, {
	        key: 'setAnimation',
	        value: function setAnimation() {
	            var _this2 = this;
	
	            this.animate = function () {
	                _this2.animateNext();
	            };
	        }
	    }, {
	        key: 'setEvent',
	        value: function setEvent() {
	            var type = this.element.getAttribute("data-animation-condition");
	
	            switch (type) {
	                case 'seen':
	                    events.addSeenItem(this);
	                    break;
	                default:
	                    console.error("Condition data attribute value is not supported. Check documentation for accepted values.", item);
	            }
	        }
	    }]);

	    return AnimationContainer;
	}();

/***/ }
/******/ ])
});
;
//# sourceMappingURL=animate-js.js.map