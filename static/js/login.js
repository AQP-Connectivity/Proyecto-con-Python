// Mostrar / ocultar contraseña
const togglePwd = document.getElementById('togglePwd');
const pwdInput = document.getElementById('password');

togglePwd.addEventListener('click', () => {
  const isPwd = pwdInput.getAttribute('type') === 'password';
  pwdInput.setAttribute('type', isPwd ? 'text' : 'password');
  togglePwd.innerHTML = isPwd
    ? '<i class="bi bi-eye-slash"></i>'
    : '<i class="bi bi-eye"></i>';
});

// Validación simple del formulario + demo de autenticación
const form = document.getElementById('formLogin');
const alerta = document.getElementById('alerta');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  if (!form.checkValidity()) {
    e.stopPropagation();
    form.classList.add('was-validated');
    alerta.classList.remove('d-none', 'alert-success');
    alerta.classList.add('alert-danger');
    alerta.textContent = 'Revisa los campos marcados.';
    return;
  }

  const email = document.getElementById('email').value.trim();
  const pass = pwdInput.value;

  const DEMO_USER = 'demo@correo.com';
  const DEMO_PASS = '123456';

  if (email === DEMO_USER && pass === DEMO_PASS) {
    alerta.classList.remove('d-none', 'alert-danger');
    alerta.classList.add('alert-success');
    alerta.textContent = '¡Inicio de sesión exitoso! Redirigiendo…';

    setTimeout(() => {
      window.location.href = "/inicio"; // ✅ redirige al dashboard principal
    }, 800);
  } else {
    alerta.classList.remove('d-none', 'alert-success');
    alerta.classList.add('alert-danger');
    alerta.textContent = 'Credenciales incorrectas. Usa demo@correo.com / 123456';
  }
});
