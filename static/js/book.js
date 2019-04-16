document.addEventListener('DOMContentLoaded', () => {

  // Set the value of the dropdown button which is used to limit search results
  let dropdown_items = document.querySelectorAll('.dropdown-item');
  for (let i = 0; i < dropdown_items.length; i++) {
    dropdown_items[i].addEventListener('click', function () {
      document.querySelector('#results_limit').value = this.dataset.results;

      // The number 42 is arbitrarily chosen to represent infinity, or all
      if (this.dataset.results !== "42") {
        document.querySelector('#dropdown-selection').innerHTML = `Show ${this.dataset.results} Results`
      } else {
        document.querySelector('#dropdown-selection').innerHTML = 'Show All'
      }
    });
  };

  // Determine whether to show the search results <div>
  let search_results_message = document.querySelector('#search-results-message');
  if (search_results_message.innerHTML !== '') {
    console.log('not empty');
    document.querySelector('#search-results').style.visibility='visible';
  } else {
    document.querySelector('#search-results').style.visibility='hidden';
  };

});