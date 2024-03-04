document.addEventListener("DOMContentLoaded", function() {
    // Your login page JavaScript code goes here

    var loginForm = document.getElementById('form-login').addEventListener('submit', function(event) {
        event.preventDefault();
    
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
    
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => {
            if (response.ok) {
                alert('Login successful!');
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
});
