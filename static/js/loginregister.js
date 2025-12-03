const retypeT = document.getElementById("retypetitle");
const retypeI = document.getElementById("retypeinput");
const p = document.querySelector("#loginregister p");
const span = document.querySelector("#loginregister p span");

span.addEventListener("click", function () {
    if (span.textContent == "Sign Up") {
        span.textContent = "Login"
        p.textContent = "Don't have an account? "
        if (retypeI.style.display == "none") menu.style.display = "flex";
        if (retypeT.style.display == "none") menu.style.display = "flex";
    }
    if (span.textContent == "Login") {
        span.textContent = "Sign Up";
        p.textContent = "Already have an account? "
        if (retypeI.style.display == "flex") menu.style.display = "none";
        if (retypeT.style.display == "flex") menu.style.display = "none";
    }
});