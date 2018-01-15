var functions = require('./functions.js');
// data-animation-type="seen" ==================================================
var seenItems = []

// check if middle pos of any item is in browser
function checkSeen () {

	for (let item of seenItems) {
		var viewTop = $(window).scrollTop();
		var viewBottom = viewTop + $(window).height();

		if ((item.middlePos <= viewBottom) && (item.middlePos >= viewTop)) {
			item.animate();
			seenItems.splice(seenItems.indexOf(item), 1);

			if (seenItems.length == 0) {
				$(window).off('scroll', this); // not properly unbinding scroll event
			}
		}
	}
}

// bind check seen items to window scroll upon adding first item
export function addSeenItem(item) {
	if (seenItems.length == 0) {
		$(window).on('scroll', checkSeen);
	}
	item.middlePos = functions.getMiddlePos(item.element);
	seenItems.push(item);
}
//==============================================================================

export function addItem(element){

}

export function checkAllItems () {
	checkSeen();
}






// on some cases, event conditions may change
// check if window resizes, then recalculate middlePos in seenItems
