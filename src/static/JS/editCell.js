document.querySelectorAll('td')
        .forEach(e => e.addEventListener('blur', saveEditCell));
document.querySelectorAll('td')
        .forEach(e => e.addEventListener('keydown', keydownListener));


async function keydownListener(evt){
    if (evt.key === "Enter" || evt.key == 'Escape') {
        evt.target.blur();
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
    var row = cell.parentElement;
    var linkText = getValsFromRow(row)['url'];
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
    var row = cell.parentElement;
    var linkText = evt.target.innerHTML;
    let id = getValsFromRow(row)['id'];
    let new_date_val = getCurrDate();

    setRowValue(row, 'url', linkText);
    cell.removeChild(evt.target);

    const send_get = await retrieveScrapedRow(id, linkText);
    if (send_get['result'] == 'true') {
        console.log("%c editing after scraping", "color:brown;");
        setRowValue(row, 'country', send_get['country']);
        setRowValue(row, 'genre', send_get['genre']);
        setRowValue(row, 'tags', send_get['tags']);
        setRowValue(row, 'date_modified', send_get['date_modified']);
        setRowValue(row, 'title', send_get['title']);
        console.log({row});
        return;
    }

    console.log('doing the other one!');
    console.log(send_get['result'])
    const server_success = await sendUrlToServer(id, "Url", linkText, new_date_val);
    if (server_success['result'] == 'true') {  
        setRowValue(row, 'date_modified', getCurrDate());
    }
}

async function retrieveScrapedRow(id, url) {
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
    
    console.log("%c retrieveScrapedRowFromServer", "color:yellow;")
    console.log({send_get});  
    return send_get;
}

async function saveEditCell(evt){
    var row = evt.target.parentElement;
    let id = getValsFromRow(row)['id'];
    let val;
    let col;
    let new_date_val = getCurrDate();

    for (let i = 0, cell; cell = row.cells[i]; i++) {
        if (cell == evt.target) {
            val = cell.children[0].innerHTML;
            col = row.parentElement.parentElement.rows[0].cells[i].innerHTML;
            if (val == "<br>") {val = "";}
            break;
        }
    }

    const send_post = await updateServerUrl(id, col, val, new_date_val);
    if (send_post['result'] == 'true') { 
        setRowValue(row, 'date_modified', getCurrDate())
    }
}

async function updateServerUrl(id, col, val, date_val) {
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

    console.log("%c updateServerUrl", "color:purple;")
    console.log({id, col, val, date_val, send_post});  
    return send_post;
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

// delete rows
// edit history
// sort
// find
// UI touches
// On focus extend row
// URL dropdown
// drag rows?