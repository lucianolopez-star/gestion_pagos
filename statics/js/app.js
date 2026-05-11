// static/js/app.js
// Espacio para JS global adicional.
// La lógica principal del formulario de evento vive en eventos/form.html (inline).

// Auto-dismiss de alertas Bootstrap después de 4 segundos
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".alert.alert-dismissible").forEach(el => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    }, 4000);
  });
});
