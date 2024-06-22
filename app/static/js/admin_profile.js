
    document.addEventListener("DOMContentLoaded", function() {
        var profileLink = document.querySelector('#profile_icon');
        var modal = document.getElementById('profileModal');
        var closeModal = document.getElementById('closeModal');
        var closeButton = document.getElementById('closeButton');

        profileLink.addEventListener('click', function(event) {
            event.preventDefault();
            modal.classList.remove('hidden');
        });

        closeModal.addEventListener('click', function() {
            modal.classList.add('hidden');
        });

        closeButton.addEventListener('click', function() {
            modal.classList.add('hidden');
        });

        // Optional: Close modal when clicking outside of it
        window.addEventListener('click', function(event) {
            if (event.target == modal) {
                modal.classList.add('hidden');
            }
        });
    });

