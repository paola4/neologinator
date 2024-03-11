const sliderEl = document.querySelector("#range")
const sliderValue = document.querySelector(".value")

sliderEl.addEventListener("input", (event) => {
  const tempSliderValue = event.target.value; 
  
  sliderValue.textContent = tempSliderValue;
  
  const progress = (tempSliderValue / sliderEl.max) * 100;
 
  sliderEl.style.background = `linear-gradient(to right, #000000 ${progress}%, #ccc ${progress}%)`;
})


function scaleHeader() {
  var scalable = document.querySelectorAll('.scale--js');
  var margin = 10;
  for (var i = 0; i < scalable.length; i++) {
    var scalableContainer = scalable[i].parentNode;
    scalable[i].style.transform = 'scale(1)';
    var scalableContainerWidth = scalableContainer.offsetWidth - margin;
    var scalableWidth = scalable[i].offsetWidth;
    scalable[i].style.transform = 'scale(' + scalableContainerWidth / scalableWidth + ')';
    scalableContainer.style.height = scalable[i].getBoundingClientRect().height + 'px';
  }
} 

// Debounce by David Walsch
// https://davidwalsh.name/javascript-debounce-function

function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

var myScaleFunction = debounce(function() {
	scaleHeader();
}, 250);

myScaleFunction();

window.addEventListener('resize', myScaleFunction);