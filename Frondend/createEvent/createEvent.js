document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-createevent');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const eventName = document.getElementById('eventname').value;
        const street = document.getElementById('street').value;
        const streetNumber = document.getElementById('streetnumber').value;
        const postalCode = document.getElementById('postalcode').value;
        const date = document.getElementById('date').value;
        const location = document.getElementById('location').value;
        const description = document.getElementById('description').value;
        const group = document.getElementById('group').value;
        const participants = document.getElementById('participants').value;
        const startingTime = document.getElementById('startingtime').value;
        const endTime = document.getElementById('endtime').value;

        // Create an object with the form data
        const formData = {
            name: eventName,
            street: street,
            street_number: streetNumber,
            city_code: postalCode,
            date: date,
            location: location,
            description: description,
            group: group,
            users: participants,
            time_start: startingTime,
            time_end: endTime
        };

        fetch('/api/appointment', {
            method: 'POST',
            body: formData
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