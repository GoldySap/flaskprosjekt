const form = document.forms["loginregister"];
const retype = document.getElementById("retyping");
const btn = document.querySelector("#loginregister button");
const p = document.querySelector("#loginregister .p");
const span = document.querySelector("#loginregister .p span");

function lr(isLogin) {
    if (isLogin) {
        btn.textContent = "Login In";
        p.innerHTML = `Don't have an account? <span class="span">Sign Up</span>`;
        retype.style.display = "none";
        form.action = "/login";
    } else {
        btn.textContent = "Sign Up";
        p.innerHTML = `Already have an account? <span class="span">Login</span>`;
        retype.style.display = "flex";
        form.action = "/registrer";
    }
}

function attachSpanListener() {
    const span = document.querySelector("#loginregister p span");
    span.addEventListener("click", () => {
        const isLogin = span.textContent === "Login";
        lr(isLogin);
        attachSpanListener();
    });
}

attachSpanListener();
