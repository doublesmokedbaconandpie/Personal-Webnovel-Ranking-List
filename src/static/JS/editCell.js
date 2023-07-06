document.querySelectorAll('td')
        .forEach(e => e.addEventListener('blur', editCell));
document.querySelectorAll('td')
        .forEach(e => e.addEventListener('keydown', keyEditCell));


async function keyEditCell(evt){
    if (evt.key === "Enter") {
        $('div[contenteditable="true"]').trigger('focus').trigger('blur');
    }
    if (evt.key === "k" && evt.ctrlKey) {
        editLinkCell(evt);
    }
}

async function editLinkCell(evt) {
    console.log(evt);
}

async function editCell(evt){
    var row = evt.target.parentElement;
    let id = row.cells[10].children[0].innerHTML;
    let val;
    let col;
    let new_date_val = getCurrDate();

    for (let i = 0; i < row.cells.length; i++) {
        if (row.cells[i] == evt.target) {
            val = row.cells[i].children[0].innerHTML;
            col = row.parentElement.parentElement.rows[0].cells[i].innerHTML;
            break;
        }
    }

    const server_success = await sendDataToServer(id, col, val, new_date_val);

    if (server_success == 'true') {
        let old_date_div = row.cells[8].children[0];
        let new_date_div = getDivCurrDate()
        row.cells[8].replaceChild(new_date_div, old_date_div);       
    }
}

async function sendDataToServer(id, col, val, date_val) {
    const send_post = await fetch(`/editCell`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            id: id,
            col: col,
            val: val,
            date_val: date_val})
        })
        .then(response => response.json());

    console.log({id, col, val, date_val, send_post});  


    if (send_post['result'] == 'false') {
        return 'false';
    }

    const send_get = await fetch(`/editCell`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
        .then(response => response.json());
    
    return send_get['result'];
}

function getDivCurrDate() {
    let currentDate = getCurrDate();

    var div = document.createElement('div');
    div.setAttribute('class', "scrollable");
    div.innerHTML = currentDate;
    return div;
}

function getCurrDate() {
    const date = new Date();
    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();
    if (String(month).length == 1) {
        month = `0${month}`
    }
    if (String(day).length == 1) {
        day = `0${day}`
    }
    return `${year}-${month}-${day}`;
}

// update row in DB
// maybe includes using the URL method to automatically populate genre tags
// delete rows
// delete cell, double click to edit?
