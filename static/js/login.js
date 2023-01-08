function email() {
    const emailW = document.getElementById('email-warning');
    const val = document.getElementById('email').value;
    if (val == "") {
        emailW.innerText = '';
        emailW.visibility = 'hidden';
        invEmail = true;
    } else if (val.indexOf('@') == -1) {
        emailW.innerText = 'Invalid Email';
        emailW.visibility = 'active';
        invEmail = true;
    } else {
        emailW.innerText = '';
        emailW.visibility = 'hidden';
        invEmail = false;
    }
    submitButton();
}

function password() {
    document.getElementById('email-warning').visibility = "hidden";
}

let invEmail = true;
document.getElementById('email').addEventListener('input', email);
document.getElementById('password').addEventListener('input', password);

function submitButton() {
    if (invEmail) {
        document.getElementById('submit').disabled = true;
    } else {
        document.getElementById('submit').disabled = false;
    }
}