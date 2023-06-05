
// Login
function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'home.html') {
            // Redirect to home.html if login is successful
            window.location.href = 'home.html';
        } else {
            // Display error message
            document.getElementById('responseText').innerText = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        console.log(error);
        document.getElementById('responseText').innerText = 'Error: ' + error;
    });
}