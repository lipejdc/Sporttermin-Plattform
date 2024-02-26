var loginForm = document.getElementById('form-registration').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('registration-username').value;
    var email = document.getElementById('registration-email').value;
    var password = document.getElementById('registration-password').value;
    var repeatPassword = document.getElementById('repeatpassword').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
            repeatPassword: repeatPassword
        })
    })
    .then(response => {
        if (response.ok) {
            alert('Registration successful!');
            // Redirect or perform other actions for successful login
        } else {
            alert('Invalid email or password.');
            // Handle login failure
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
