document.querySelectorAll('td')
        .forEach(e => e.addEventListener('blur', saveEditCell));
document.querySelectorAll('td')
        .forEach(e => e.addEventListener('keydown', keydownListener));


async function keydownListener(evt){
    if (evt.key === "Enter") {
        $('div[contenteditable="true"]').trigger('focus').trigger('blur');
    }
    if (evt.key === "k" && evt.ctrlKey) {
        evt.preventDefault();
        evt.stopPropagation();
        if (evt.target.parentElement.className != 'col2'){return;}
        if (evt.target.parentElement.children[2] == evt.target){return;}
        editLinkCell(evt);
    }
}

async function editLinkCell(evt) {
    console.log("%c editLinkCell", "color:red;");
    console.log(evt);

    var cell = evt.target.parentElement;
    console.log({"cell": cell, "evt":evt.target});
    var linkText = cell.children[0].children[0].getAttribute("href");
    var linkEditor = createLinkEditor(linkText);
    cell.appendChild(linkEditor);
    linkEditor.focus();
}

function createLinkEditor(text) {
    var div = document.createElement('div');
    var txt = document.createTextNode(text);
    div.appendChild(txt);
    div.setAttribute("class", 'link-editor');
    div.setAttribute("contenteditable", "true");
    div.addEventListener('blur', exitLinkEditor);
    return div;
}

async function exitLinkEditor(evt) {
    console.log("%c exitLinkEditor", "color:blue;");
    console.log(evt);
    var cell = evt.target.parentElement;
    var linkText = evt.target.innerHTML;
    cell.children[0].children[0].setAttribute("href", linkText);
    cell.children[1].children[0].setAttribute("href", linkText);
    cell.removeChild(evt.target);

    var row = cell.parentElement;
    let id = row.cells[10].children[0].innerHTML;
    let new_date_val = getCurrDate();

    const send_get = await retrieveDataFromServer(id, linkText);
    if (send_get['result'] == 'true') {
        console.log("%c editing after scraping", "color:brown;");
        console.log({row});
        console.log({'a': row.cells[1].children[0], 'b': row.cells[1].children[0].innerHTML})
        row.cells[1].children[0].innerHTML = send_get['country'];
        row.cells[6].children[0].innerHTML = send_get['genre'];
        row.cells[7].children[0].innerHTML = send_get['tags'];
        row.cells[8].children[0].innerHTML = send_get['date_modified'];
        row.cells[2].children[0].children[0].innerHTML = send_get['title'];
        row.cells[2].children[1].children[0].innerHTML = send_get['title'];
        console.log({row});
        return;
    }

    const server_success = await sendDataToServer(id, "Url", linkText, new_date_val);
    if (server_success['result'] == 'true') {  
        row.cells[8].children[0].innerHTML = getCurrDate();
    }
}

async function retrieveDataFromServer(id, url) {
    console.log(`Sending id ${id} and url ${url}`);
    const send_get = await fetch(`/fetchScrapedRow`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            id: id,
            url: url})
    })
        .then(response => response.json());
    
    console.log("%c Get Data", "color:yellow;")
    console.log({send_get});  
    return send_get;
}

async function saveEditCell(evt){
    var row = evt.target.parentElement;
    let id = row.cells[10].children[0].innerHTML;
    let val;
    let col;
    let new_date_val = getCurrDate();

    for (let i = 0; i < row.cells.length; i++) {
        if (row.cells[i] == evt.target) {
            val = row.cells[i].children[0].innerHTML;
            col = row.parentElement.parentElement.rows[0].cells[i].innerHTML;
            if (val == "<br>") {val = "";}
            break;
        }
    }

    const send_post = await sendDataToServer(id, col, val, new_date_val);
    if (send_post['result'] == 'true') {
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

    console.log("%c Post Data", "color:purple;")
    console.log({id, col, val, date_val, send_post});  
    return send_post;
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

// maybe includes using the URL method to automatically populate genre tags
// delete rows
// delete cell, double click to edit?
