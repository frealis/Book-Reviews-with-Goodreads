document.addEventListener('DOMContentLoaded', function() {

  console.log('dom content loaded');
  document.querySelector('.register-button').disabled = true;

  const register_password = document.querySelector('#register_password')
  const register_password_again = document.querySelector('#register_password_again')

  register_password.addEventListener('keyup', passwordsMatch);
  register_password_again.addEventListener('keyup', passwordsMatch);

  function passwordsMatch() {
    console.log('register_password.value: ', register_password.value)
    console.log('register_password_again.value: ', register_password_again.value)

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