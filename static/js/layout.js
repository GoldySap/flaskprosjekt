$(document).ready(function () {
    $("li").on("click", function () {
        let route = this.id;
        let dataToSend = { 'param': `${route}` };
        $.ajax({
            url: '/routing',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(dataToSend),
            success: function(response) {
                console.log('Success:', response);
                alert(response.message);
                location.reload();
            },
            error: function(error) {
                console.log('Error:', error);
                alert('An error occurred.');
            }
        });
    });
});
