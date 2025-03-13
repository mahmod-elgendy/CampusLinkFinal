// main.js
document.getElementById('updateForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const userId = 'UserID3';  // Replace this with the dynamic user ID as needed
    const updatedData = {
        UserName: document.getElementById('name').value,
        UserEmail: document.getElementById('email').value,
        UserBio: document.getElementById('bio').value,
        UserPFP: document.getElementById('pfp').value
    };

    fetch(`/profile/update/submit/${userId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Include CSRF token
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display success message
        window.location.href = `/profile/${userId}/`; // Redirect to profile page after update
    })
    .catch(error => console.error('Error updating profile:', error));
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function deletePost(postId) {
    // Get CSRF token from the meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    fetch(`/delete-post/${postId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Use the CSRF token from the meta tag
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);  // Success message
            location.reload();  // Reload the page to reflect changes
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the post.');
    });
}
