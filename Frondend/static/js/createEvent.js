document.addEventListener('DOMContentLoaded', function() {
    fetch('/user/')
    .then(response => response.text())
    .then(data => {
        document.getElementById('userName').innerText = data;
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-createevent');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const eventName = document.getElementById('eventname').value;
        const street = document.getElementById('street').value;
        const streetNumber = document.getElementById('streetnumber').value;
        const postalCode = document.getElementById('postalcode').value;
        const date = document.getElementById('date').value;
        const city = document.getElementById('city').value;
        const description = document.getElementById('description').value;
        const group = document.getElementById('group').value;
        const numberOfParticipants = document.getElementById('participants').value;
        const startingTime = document.getElementById('startingtime').value;
        const endTime = document.getElementById('endtime').value;

        // Create an object with the form data
        const formData = {
            name: eventName,
            street: street,
            housenr: streetNumber,
            citycode: postalCode,
            date: date,
            city: city,
            notice: description,
            friendzone_id: 1,
            maxUser: numberOfParticipants,
            time_start: startingTime,
            time_stop: endTime
        };

        fetch('/api/appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                alert('lalala!');
                // Redirect or perform other actions for successful login
            } else {
                alert('lelele!');
                // Handle login failure
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});