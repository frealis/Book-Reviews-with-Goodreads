document.addEventListener('DOMContentLoaded', () => {

  // Set the value of the '#results_limit' <div>, which is ultimately used to 
  // limit the number of search results. This method basically stores variables
  // in hidden <div> elements which.
  let dropdown_items = document.querySelectorAll('.dropdown-item');
  for (let i = 0; i < dropdown_items.length; i++) {
    dropdown_items[i].addEventListener('click', function () {
      document.querySelector('#results_limit').value = this.dataset.results;

      // Update the dropdown selection button text to reflect the maximum number,
      // or limit, of displayed search results. The number 42 is arbitrarily chosen 
      // to represent no limit.
      if (this.dataset.results !== "42") {
        document.querySelector('#dropdown-selection').innerHTML = `Show ${this.dataset.results} Results`
      } else {
        document.querySelector('#dropdown-selection').innerHTML = 'Show All'
      }
    });
  };

  // Rate the book that is currently being viewed on a scale from 1 to 5 stars --
  // the result is stored in a hidden <div>.
  let rating_stars = document.querySelectorAll('.rating-stars');
  for (let i = 0; i < rating_stars.length; i++) {
    rating_stars[i].addEventListener('click', function () {

      // Change the actual rating that eventually gets sent to the backend.
      document.querySelector('#rating-selection').value = this.dataset.rating;

      // Determine whether the selected rating star is a Font Awesome 
      // regular/outline (far) or solid (fas).
      current_fa = ''
      for (let j = 0; j < document.querySelector('#' + this.id).classList.length; j++) {
        if (document.querySelector('#' + this.id).classList[j] === 'far') {
          current_fa = 'far';
        } else if (document.querySelector('#' + this.id).classList[j] === 'fas') {
          current_fa = 'fas';
        };
      };

      // Toggle the selected Font Awesome star icons between the 'far' (font 
      // awesome regular, aka 'outline') or the 'fas' (font awesome solid) class
      // to represent current star rating.
      // https://stackoverflow.com/questions/6791112/how-to-filter-elements-returned-by-queryselectorall
      let stars_less_than = Array.from(document.querySelectorAll('.rating-stars')).filter(star => star.dataset.rating < this.dataset.rating)
      let stars_more_than = Array.from(document.querySelectorAll('.rating-stars')).filter(star => star.dataset.rating > this.dataset.rating)

      if (current_fa === 'far') {
        document.querySelector('#' + this.id).classList.remove('far');
        document.querySelector('#' + this.id).classList.add('fas');
        for (k = 0; k < stars_less_than.length; k++) {
          stars_less_than[k].classList.remove('far');
          stars_less_than[k].classList.add('fas')
        };
      } else if (current_fa = 'fas') {
        for (k = 0; k < stars_more_than.length; k++) {
          stars_more_than[k].classList.remove('fas');
          stars_more_than[k].classList.add('far')
        };
      };
    });
  };

  // Generate the HTML footer elements
  var fbw = document.createElement('div');
  fbw.setAttribute('id', 'footer-background-wrapper');
  var fb = document.createElement('div');
  fb.setAttribute('id', 'footer-background');
  var ftw = document.createElement('div');
  ftw.setAttribute('id', 'footer-text-wrapper');
  var ft = document.createElement('a');
  ft.setAttribute('id', 'footer-text');
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

  // Access API Modal
  // https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_modal2

  // When the user clicks the 'Access Api' link, open the modal 
  var access_api_link = document.querySelector("#access_api");
  access_api_link.onclick = function() {
    modal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  var span = document.getElementsByClassName("close")[0];
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  var modal = document.querySelector('#access_api_modal');
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    };
  }

});