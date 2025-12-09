document.addEventListener("DOMContentLoaded", () => {
    const menu = document.querySelector(".menu");
    document.querySelectorAll("#headerbuttons button").forEach(btn => {
        btn.addEventListener("click", () => {
            const display = getComputedStyle(menu).display;
            menu.style.display = display === "none" ? "flex" : "none";
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