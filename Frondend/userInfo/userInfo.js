document.addEventListener("DOMContentLoaded", function() {

    const editProfileBtn = document.getElementById('editProfileBtn');
    const profileInfo = document.getElementById('profileInfo');
    const editProfileForm = document.getElementById('editProfileForm');
    const cancelEditBtn = document.getElementById('cancelEditBtn');

    editProfileBtn.addEventListener('click', () => {
        
        // Retrieve user data from the profile
        const firstName = document.getElementById('firstName').textContent;
        const lastName = document.getElementById('lastName').textContent;
        const email = document.getElementById('email').textContent;
        const gender = document.getElementById('gender').textContent;
        const age = document.getElementById('age').textContent; 
        const city = document.getElementById('city').textContent; 

        // Populate the input fields in the edit profile form with the retrieved user data
        document.getElementById('editFirstName').value = firstName;
        document.getElementById('editLastName').value = lastName;
        document.getElementById('editEmail').value = email;
        document.getElementById('editGender').value = gender; // Assuming there's an input field with id 'editGender'
        document.getElementById('editAge').value = age; // Assuming there's an input field with id 'editAge'
        document.getElementById('editCity').value = city; // Assuming there's an input field with id 'editCity'

        // Show the edit profile form
        profileInfo.style.display = 'none';
        editProfileForm.classList.remove('d-none');
    });

    editProfileForm.addEventListener('submit', (event) => {
        event.preventDefault();

        // Get updated user data from the input fields
        const updatedFirstname = document.getElementById('editFirstName').value;
        const updatedLastName = document.getElementById('editLastName').value;
        const updatedEmail = document.getElementById('editEmail').value;
        const updatedGender = document.getElementById('editGender').value;
        const updatedAge = document.getElementById('editAge').value;
        const updatedCity = document.getElementById('editCity').value;

        // Create a data object to send to the server
        const userData = {
            firstName: updatedFirstname,
            lastName: updatedLastName,
            email: updatedEmail,
            gender: updatedGender,
            age: updatedAge,
            city: updatedCity
        };

        // Send the data to the server using fetch API or any other method
        fetch('/api/user', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => {
            if (response.ok) {
                // Optionally, update the displayed user data with the updated values
                document.getElementById('userName').textContent = updatedUsername;
                document.getElementById('fullName').textContent = updatedFullName;
                document.getElementById('email').textContent = updatedEmail;
                document.getElementById('gender').textContent = updatedGender;
                document.getElementById('age').textContent = updatedAge;
                document.getElementById('city').textContent = updatedCity;

                // Hide the editProfileForm and show the profileInfo
                profileInfo.style.display = 'block';
                editProfileForm.classList.add('d-none');
            } 
            
            else {
                console.error('Failed to update profile:', response.statusText);
            }
        });
    });

    cancelEditBtn.addEventListener('click', () => {
        profileInfo.style.display = 'block';
        editProfileForm.classList.add('d-none');
    });
});
