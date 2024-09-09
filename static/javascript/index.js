document.getElementById('loginButton').addEventListener('click', () => {
    window.location.href = 'registration_login.html'; 
});

document.querySelectorAll('.service-box').forEach(box => {
    box.addEventListener('click', function() {
        alert('You clicked on ' + this.querySelector('span').textContent);
    });
});


document.querySelectorAll('.service-box').forEach(box => {
    box.addEventListener('click', function() {
        window.location.href = '../frontend/jobs.html'; // Replace with the actual path to your Jobs page
    });
});


