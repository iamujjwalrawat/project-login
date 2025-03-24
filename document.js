document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // AJAX request
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://example.com/api/login', true); // Replace with your API endpoint
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            document.getElementById('message').textContent = 'Login successful!';
            // Handle successful login (e.g., redirect or store token)
        } else {
            document.getElementById('message').textContent = 'Login failed. Please try again.';
        }
    };

    xhr.onerror = function() {
        document.getElementById('message').textContent = 'An error occurred. Please try again.';
    };

    const data = JSON.stringify({ username: username, password: password });
    xhr.send(data);
});