$(document).ready(function
    // Clear the input field and perform actions
    $('#search-form').on('submit', function() {
        const query = $('input[name="query"]').val();
        if (query.length > 0) {
            alert('Searching for: ' + query);  // Placeholder alert
        }
    });
});
