document.addEventListener('DOMContentLoaded', function() {

  console.log('dom content loaded');

  error_login = document.querySelector('.error-login').innerHTML

  if (error_login !== '') {
    // document.querySelector('.error-login').classList.add('alert');
    // document.querySelector('.error-login').classList.add('alert-danger');
  }

});