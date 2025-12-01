document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("header button").forEach(btn => {
        btn.addEventListener("click", function () {
            document.querySelector(".menu").classList.toggle("hidden", true);
        });
    });

    document.querySelectorAll("li").forEach(li => {
        li.addEventListener("click", function () {
            let route = this.id;

            $.ajax({
                url: '/routing',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ param: route }),
                success: function (response) {
                    if (response.redirect) {
                        window.location.href = response.redirect;
                        return;
                    }
                    alert(response.message || "Done");
                },
                error: function (error) {
                    console.log("Error:", error);
                    alert("An error occurred.");
                }
            });
        });
    });

});
