document.getElementById('togglePassword').addEventListener('click', function () {
  var passwordInput = document.getElementById('id_password');
  var toggleIcon = document.getElementById('toggleIcon');
  
  if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      toggleIcon.classList.remove('bi-eye-slash');
      toggleIcon.classList.add('bi-eye');
  } else {
      passwordInput.type = 'password';
      toggleIcon.classList.remove('bi-eye');
      toggleIcon.classList.add('bi-eye-slash');
  }
});
