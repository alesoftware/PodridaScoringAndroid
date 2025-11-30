/**
 * Oh Hell! Scorer - Client-Side JavaScript
 * Handles dynamic interactions and UI enhancements
 */

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(flash => {
        setTimeout(() => {
            flash.style.transition = 'opacity 0.5s';
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 500);
        }, 5000);
    });
});

// Touch feedback for buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn, .player-button, .hand-button, .spreadsheet-item');
    
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.style.opacity = '0.7';
        });
        
        button.addEventListener('touchend', function() {
            this.style.opacity = '1';
        });
    });
});

// Prevent double-tap zoom on buttons (iOS)
document.addEventListener('DOMContentLoaded', function() {
    let lastTouchEnd = 0;
    
    document.addEventListener('touchend', function(event) {
        const now = Date.now();
        if (now - lastTouchEnd <= 300) {
            event.preventDefault();
        }
        lastTouchEnd = now;
    }, false);
});

// Helper function for AJAX requests
function sendRequest(url, data, callback) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(data)
    })
    .then(response => response.json())
    .then(callback)
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}

// Confirm dialogs for destructive actions
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Initialize hand button selection visuals
document.addEventListener('DOMContentLoaded', function() {
    const handButtons = document.querySelectorAll('.hand-button');
    
    handButtons.forEach(button => {
        const checkbox = button.querySelector('input[type="checkbox"]');
        if (checkbox && checkbox.checked) {
            button.classList.add('selected');
        }
    });
});

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}
