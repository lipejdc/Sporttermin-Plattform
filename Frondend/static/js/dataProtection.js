document.addEventListener('DOMContentLoaded', function() {
    fetch('/user/')
    .then(response => response.text())
    .then(data => {
        document.getElementById('userName').innerText = data;
    });
});
