document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Validate email format
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        document.getElementById('message').textContent = 'Please enter a valid email address.';
        return;
    }

    // Simulate an AJAX request (GET and PUT)
    const url = 'https://example.com/api/login'; // Replace with your API endpoint

    // Example of a GET request (to fetch user data)
    fetch(url + '?email=' + encodeURIComponent(email))
        .then(response => response.json())
        .then(data => {
            // Simulate a successful login for specific credentials
            if (data.email === email && data.password === password) {
                document.getElementById('message').textContent = 'Login successful!';
                document.getElementById('message').style.color = 'green';
            } else {
                document.getElementById('message').textContent = 'Login failed. Please try again.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('message').textContent = 'An error occurred. Please try again.';
        });

    // Example of a PUT request (to update user data)
    const userData = {
        email: email,
        password: password
    };

    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
