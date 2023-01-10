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

function password() {
    const passwordW = document.getElementById('password-warning');
    const val = document.getElementById('password').value;
    if (val == "") {
        passwordW.innerText = '';
        passwordW.setAttribute("hidden", "");
        invPassword = false;
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
let invPassword = false;
document.getElementById('name').addEventListener('input', nameC);
document.getElementById('password').addEventListener('input', password);

function submitButton() {
    if (invName || invPassword) {
        document.getElementById('save').disabled = true;
    } else {
        document.getElementById('save').disabled = false;
    }
}