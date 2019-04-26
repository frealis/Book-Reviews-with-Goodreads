document.addEventListener('DOMContentLoaded', function() {

  // Disable the "Register" button by default
  document.querySelector('.btn-register').disabled = true;

  // Create constants for 'Create an account' password input fields
  const register_password = document.querySelector('#register_password')
  const register_password_again = document.querySelector('#register_password_again')

  // Assign 'keyup' event listeners to the 'Create an account' password input 
  // fields
  register_password.addEventListener('keyup', passwordsMatch);
  register_password_again.addEventListener('keyup', passwordsMatch);

  // Determine whether the client-entered passwords match, and enable 'Register'
  // button if so. Also display messages in the DOM to let the client know
  // whether or not their passwords match
  function passwordsMatch() {
    if (register_password.value.length !== 0 && register_password_again.value.length !== 0) {
      if (register_password.value === register_password_again.value) {
        document.querySelector('.btn-register').disabled = false;
        document.querySelector('#passwords_match').classList.add('passwords-match')
        document.querySelector('#passwords_match').classList.remove('passwords-dont-match')
        document.querySelector('#passwords_match').innerHTML = 'Password match!'
      } else {
        document.querySelector('.btn-register').disabled = true;
        document.querySelector('#passwords_match').classList.add('passwords-dont-match')
        document.querySelector('#passwords_match').classList.remove('passwords-match')
        document.querySelector('#passwords_match').innerHTML = 'Passwords do not match.'
      };
    } else {
      document.querySelector('#passwords_match').innerHTML = ''
    };
  }

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

  console.log('footer')

});