document.addEventListener('DOMContentLoaded', function() {

  // Disable the "Register" button by default
  document.querySelector('.register-button').disabled = true;

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
        document.querySelector('.register-button').disabled = false;
        document.querySelector('#passwords_match').classList.add('passwords-match')
        document.querySelector('#passwords_match').classList.remove('passwords-dont-match')
        document.querySelector('#passwords_match').innerHTML = 'Password match!'
      } else {
        document.querySelector('.register-button').disabled = true;
        document.querySelector('#passwords_match').classList.add('passwords-dont-match')
        document.querySelector('#passwords_match').classList.remove('passwords-match')
        document.querySelector('#passwords_match').innerHTML = 'Passwords do not match.'
      };
    } else {
      document.querySelector('#passwords_match').innerHTML = ''
    };
  }

});