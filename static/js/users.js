function setShowField() {
    showFields = []
    let getFields = document.getElementsByClassName('get-fields');
    for (let i = 0; i < getFields.length; i++) {
        if (getFields[i].checked) {
            showFields.push(getFields[i].value);
        }
    }
    getUsers();
    setOrderBys();
}

let orderI = 0
let data = []
let showFields = []
document.getElementById("btn-find-user").addEventListener('click', getUsers)
document.getElementById('user-name-input').addEventListener('input', getUsers)
document.getElementById('field-vals').addEventListener('change', getUsers)
document.getElementById('op-vals').addEventListener('change', getUsers)
document.getElementById('order-vals').addEventListener('change', show)
document.getElementById('order-reverse').addEventListener('change', show)

let getFields = document.getElementsByClassName('get-fields');
for (let i = 0; i < getFields.length; i++) {
    getFields[i].addEventListener('change', setShowField);
}
setShowField()


function order(a, b) {
    if (a[orderI] === b[orderI]) {
        return 0;
    }
    return (a[orderI] < b[orderI]) ? -1 : 1;
}


function show() {
    let orderVal = document.getElementById('order-vals').value;
    orderI = showFields.indexOf(orderVal)
    data.sort(order)
    if (document.getElementById('order-reverse').checked) {
        data.reverse()
    }
    let tableFieldsData = ''
    showFields.forEach(element => {
        tableFieldsData += `<th>${element}</th>`
    });
    let tableBodyData = ''
    data.forEach(d => {
        tableBodyData += '<tr>'
        d.forEach(element => {
            tableBodyData += `<td>${element}</td>`
        });
        tableBodyData += '</tr>'
    });
    document.getElementById("table-fields").innerHTML = tableFieldsData;
    document.getElementById("table-body").innerHTML = tableBodyData;
}


function getUsers() {
    let startTime = new Date().getTime() / 1000;
    let field = document.getElementById('field-vals').value;
    let op = document.getElementById('op-vals').value;
    let val = '';
    if (op == 'LIKE') {
        val = `%${document.getElementById('user-name-input').value}%`;
    } else {
        val = document.getElementById('user-name-input').value;
    }

    let bodyData = JSON.stringify({
        'conditions': [
            [field, op, val]
        ],
        'fields': showFields
    })

    fetch(`${window.origin}/users`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: bodyData
    }).then(response => response.json()).then(function(users) {
        data = users;
        show();
    });
}

function setOrderBys() {
    content = ''
    showFields.forEach(field => {
        content += `<option value="${field}">${field}</option>`
    });
    document.getElementById("order-vals").innerHTML = content;
}