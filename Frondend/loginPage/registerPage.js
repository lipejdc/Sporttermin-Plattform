document.addEventListener("DOMContentLoaded", function() {

    var registrationForm = document.getElementById('form-registration').addEventListener('submit', function(event) {
        event.preventDefault();
    
        var firstName = document.getElementById('registration-firstname').value;
        var lastName = document.getElementById('registration-lastname').value;
        var gender = document.getElementById('registration-gender').value;
        var age = document.getElementById('registration-age').value;
        var city = document.getElementById('registration-city').value;
        var registrationEmail = document.getElementById('registration-email').value;
        var password = document.getElementById('registration-password').value;
        var repeatPassword = document.getElementById('repeatpassword').value;
    
        if (password !== repeatPassword) {
            console.log("Passwords do not match!");
            alert('Passwords do not match');
            event.preventDefault(); // Prevent form submission if passwords do not match
        }
    
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                firstname: firstName,
                lastname: lastName,
                gender: gender,
                age: age,
                city: city,
                email: registrationEmail,
                password: password
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
});