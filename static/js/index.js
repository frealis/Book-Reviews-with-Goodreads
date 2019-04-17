document.addEventListener('DOMContentLoaded', () => {

  // Set the value of the results_limit <div>, which is ultimately used to limit 
  // the number of search results.
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

  // Determine whether to show the search results <div>.
  let search_results_message = document.querySelector('#search-results-message');
  if (search_results_message.innerHTML !== '') {
    document.querySelector('#search-results').style.visibility='visible';
  } else {
    // document.querySelector('#search-results').style.visibility='hidden';
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

});