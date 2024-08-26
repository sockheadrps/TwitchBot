document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.querySelector('.overlay-container');

    if (overlay) {
        // Function to show the overlay
        function showOverlay() {
            // Fetch user data and update the table
            fetch('/users')
                .then(response => response.json())
                .then(data => {
                    if (data.users) {
                        const top10Users = data.users
                            .sort((a, b) => b.points - a.points) // Sort by points in descending order
                            .slice(0, 10); // Get top 10 users

                        const tableBody = document.querySelector('#highscore-table tbody');
                        if (tableBody) { // Check if the table body exists
                            tableBody.innerHTML = ''; // Clear existing rows

                            top10Users.forEach(user => {
                                const row = document.createElement('tr');
                                
                                row.innerHTML = `
                                    <td>${user.username}</td>
                                    <td>${user.points}</td>
                                    <td>${user.level}</td>
                                `;
                                
                                tableBody.appendChild(row);
                            });
                        } else {
                            console.error('Table body not found');
                        }
                    } else {
                        console.error('Error fetching users:', data.error);
                    }
                })
                .catch(error => console.error('Error:', error));

            // Show the overlay with a fade-in effect
            overlay.style.display = 'block';
            setTimeout(() => {
                overlay.classList.add('visible');
            }, 10); // Slight delay to ensure display is set before opacity transition
        }

        // Function to hide the overlay
        function hideOverlay() {
            // Hide the overlay with a fade-out effect
            overlay.classList.remove('visible');
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 1000); // Match the CSS transition duration
        }

        // Show the overlay initially
        showOverlay();

        // Set intervals to show and hide the overlay
        setInterval(() => {
            showOverlay();
            setTimeout(hideOverlay, 10000); // Show for 10 seconds
        }, 30000); // Repeat every 30 seconds (10 seconds visible + 20 seconds hidden)
    } else {
        console.error('Overlay container not found');
    }
});
