// Generate the HTML footer elements
var fbw = document.createElement('div');
fbw.setAttribute('id', 'footer-background-wrapper');
var fb = document.createElement('div');
fb.setAttribute('id', 'footer-background');
var ftw = document.createElement('div');
ftw.setAttribute('id', 'footer-text-wrapper');
var ft = document.createElement('a');
ft.setAttribute('class', 'btn');
ft.setAttribute('href', '#');

ft.innerHTML = "Back To Top";
ftw.appendChild(ft);
fb.appendChild(ftw);
fbw.appendChild(fb);

// Once the page has loaded, check to see if the viewport is taller than
// the document itself, and if so then add a margin to the top of the 
// footer so that it appears at the bottom of the page, then subtract
// some pixels to account for the height of the footer
extra_space = window.innerHeight - document.body.offsetHeight - 127
if (extra_space > 0) {
  document.querySelector('#footer').setAttribute('style', 'margin: ' + extra_space + 'px 0 10px 0')
} else {
  document.querySelector('#footer').setAttribute('style', 'margin: 10px 0')
};

// Add the footer to the DOM
document.querySelector('#footer').appendChild(fbw);