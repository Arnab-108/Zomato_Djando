// script.js
document.addEventListener('DOMContentLoaded', () => {
    const availabilityElements = document.querySelectorAll('.availability');

    availabilityElements.forEach(element => {
        element.addEventListener('click', () => {
            element.classList.toggle('available');
            element.classList.toggle('unavailable');
            const newAvailability = element.classList.contains('available') ? 'yes' : 'no';
            // Use AJAX to send the updated availability to the server (Django backend)
            // Update the availability in the database
        });
    });
});
