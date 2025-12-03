document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("header button").forEach(btn => {
        btn.addEventListener("click", function () {
            menu = document.getElementById("menu")
            if (menu.style.display == "none") menu.style.display = "flex";
            if (menu.style.display == "flex") menu.style.display = "none";
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
