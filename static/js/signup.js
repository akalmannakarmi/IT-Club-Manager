function nameC() {
    const nameW = document.getElementById('name-warning');
    const val = document.getElementById('name').value;
    if (val == "") {
        nameW.innerText = '';
        nameW.setAttribute("hidden", "");
        invName = true;
    } else if (val.length < 3) {
        nameW.innerText = "Name can't be less than 3 characters";
        nameW.removeAttribute("hidden");
        invName = true;
    } else {
        nameW.innerText = '';
        nameW.setAttribute("hidden", "");
        invName = false;
    }
    submitButton();
}

function email() {
    const emailW = document.getElementById('email-warning');
    const val = document.getElementById('email').value;
    if (val == "") {
        emailW.innerText = '';
        emailW.setAttribute("hidden", "");
        invEmail = true;
    } else if (val.indexOf('@') == -1) {
        emailW.innerText = 'Invalid Email';
        emailW.removeAttribute("hidden");
        invEmail = true;
    } else {
        emailW.innerText = '';
        emailW.setAttribute("hidden", "");
        invEmail = false;
    }
    submitButton();
}

function password() {
    const passwordW = document.getElementById('password-warning');
    const val = document.getElementById('password').value;
    if (val == "") {
        passwordW.innerText = '';
        passwordW.setAttribute("hidden", "");
        invPassword = true;
    } else if (val.length < 10) {
        passwordW.innerText = 'Password must be atleast 10 characters';
        passwordW.removeAttribute("hidden");
        invPassword = true;
    } else {
        passwordW.innerText = '';
        passwordW.setAttribute("hidden", "");
        invPassword = false;
    }
    submitButton();
}

let invName = true;
let invEmail = true;
let invPassword = true;
document.getElementById('name').addEventListener('input', nameC);
document.getElementById('email').addEventListener('input', email);
document.getElementById('password').addEventListener('input', password);

function submitButton() {
    if (invEmail || invName || invPassword) {
        document.getElementById('submit').disabled = true;
    } else {
        document.getElementById('submit').disabled = false;
    }
}