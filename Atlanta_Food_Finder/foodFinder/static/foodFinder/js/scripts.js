// scripts.js code
document.getElementById('registration-form').addEventListener('submit', function(event) {
    const password = document.getElementById('password').value;
    const password2 = document.getElementById('password2').value;

    if (password !== password2) {
        event.preventDefault();  // Prevent form submission
        alert("Passwords do not match.");  // Display an alert
    }
});
