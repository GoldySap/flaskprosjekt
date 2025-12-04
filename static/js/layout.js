document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("header button").forEach(btn => {
        btn.addEventListener("click", () => {
            menu = document.getElementById("menu")
            if (menu.style.display == "none") menu.style.display = "flex";
            else if (menu.style.display == "flex") menu.style.display = "none";
        });
    });
    document.querySelectorAll("li").forEach(li => {
        li.addEventListener("click", () => {
            let route = li.id;

            $.ajax({
                url: '/routing',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ param: route }),
                success: (response) => {
                    if (response.redirect) {
                        window.location.href = response.redirect;
                        return;
                    }
                    alert(response.message || "Done");
                },
                error: (error) => {
                    console.log("Error:", error);
                    alert("An error occurred.");
                }
            });
        });
    });
});