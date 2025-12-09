const tabs = document.querySelectorAll('.tab');
const sections = document.querySelectorAll('.section');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.target).classList.add('active');
    });
});

function post(url, data) {
    return fetch(url, {
        method: "POST",
        body: data
    });
}

infoForm.addEventListener("submit", e => {
    e.preventDefault();
    post("/profile/update", new FormData(infoForm))
        .then(() => alert("Profile updated!"));
});

bankForm.addEventListener("submit", e => {
    e.preventDefault();
    post("/profile/bank", new FormData(bankForm))
        .then(() => alert("Bank info saved!"));
});

billingForm.addEventListener("submit", e => {
    e.preventDefault();
    post("/profile/billing", new FormData(billingForm))
        .then(() => alert("Billing info saved!"));
});

passwordForm.addEventListener("submit", e => {
    e.preventDefault();
    post("/profile/password", new FormData(passwordForm))
        .then(() => alert("Password updated!"));
});

deleteBtn.addEventListener("click", () => {
    if (!confirm("Are you sure?")) return;

    post("/profile/delete", new FormData())
        .then(() => {
            alert("Account deleted.");
            window.location = "/logout";
        });
});
