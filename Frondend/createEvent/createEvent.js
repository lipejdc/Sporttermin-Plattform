document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-createevent');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const formData = new FormData(form); // Create a FormData object from the form
        // You can now send the formData to the server using fetch or XMLHttpRequest
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