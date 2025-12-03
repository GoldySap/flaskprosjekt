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

infoForm.onsubmit = (e) => {
e.preventDefault();
alert("Profile information saved!");
};


billingForm.onsubmit = (e) => {
e.preventDefault();
alert("Billing info saved!");
};


passwordForm.onsubmit = (e) => {
e.preventDefault();
alert("Password updated!");
};


deleteBtn.onclick = () => {
if (confirm("Are you sure you want to delete your account?")) {
alert("Account deleted.");
}
};