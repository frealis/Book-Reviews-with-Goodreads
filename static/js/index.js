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
    document.querySelector('#search-results').style.visibility='hidden';
  };

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