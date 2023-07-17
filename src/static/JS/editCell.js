document.querySelectorAll('#NovelTable td')
        .forEach(e => e.addEventListener('blur', saveEditCell));
document.querySelectorAll('#NovelTable td')
        .forEach(e => e.addEventListener('keydown', cellKeyDown));
document.querySelectorAll('#NovelTable td div')
        .forEach(e => e.addEventListener('blur', titleEditor));
document.querySelectorAll('#NovelTable td div')
        .forEach(e => e.addEventListener('keydown', titleKeyDown));

function titleKeyDown(evt) {
    if (evt.key === "Enter" || evt.key == 'Escape') {
        evt.target.blur();
    }
}

async function titleEditor(evt) {
    new_evt = Object();
    new_evt.target = evt.target.parentElement;
    await saveEditCell(new_evt);
}

async function cellKeyDown(evt){
    if (evt.key === "Enter" || evt.key == 'Escape') {
        evt.target.blur();
    }
    if (evt.key === "k" && evt.ctrlKey) {
        evt.preventDefault();
        evt.stopPropagation();
        if (evt.target.parentElement.className != 'col2'){return;}
        if (evt.target.parentElement.children[2] == evt.target){return;}
        await editLinkCell(evt);
    }
}

async function editLinkCell(evt) {
    console.log("%c editLinkCell", "color:red;");
    console.log(evt);

    const cell = evt.target.parentElement;
    const row = cell.parentElement;
    addLinkAttributeToTitle(cell);
    const linkText = getValsFromRow(row)['url'];
    const linkEditor = createLinkEditor(linkText);
    cell.appendChild(linkEditor);
    linkEditor.focus();
}

function addLinkAttributeToTitle(cell) {
    if (!cell.children[0].querySelector("a")) {
        for (let i = 0; i < 2; i++) {
            let currText = cell.children[i].innerHTML;
            let currDiv = cell.children[i];
            let origLink = document.createElement('a');
            origLink.innerHTML = currText;
            currDiv.innerHTML = "";
            currDiv.appendChild(origLink);
        }
    }     
}

function createLinkEditor(text) {
    const div = document.createElement('div');
    const txt = document.createTextNode(text);
    div.appendChild(txt);
    div.setAttribute("class", 'link-editor');
    div.setAttribute("contenteditable", "true");
    div.addEventListener('blur', exitLinkEditor);
    return div;
}

async function exitLinkEditor(evt) {
    console.log("%c exitLinkEditor", "color:blue;");
    console.log(evt);

    const cell = evt.target.parentElement;
    const row = cell.parentElement;
    const linkText = evt.target.innerHTML;
    const id = getValsFromRow(row)['id'];
    const new_date_val = getCurrDate();

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

    console.log('Scrape failed, just sending url');
    console.log(send_get['result'])
    const server_success = await updateServerUrl(id, "Url", linkText, new_date_val);
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
    console.log("%c saveEditCell", "color:pink;")
    const row = evt.target.parentElement;
    const row_vals = getValsFromRow(row);
    console.log(row_vals);
    const id = row_vals['id'];
    const new_date_val = getCurrDate();

    let val, col, i, cell;
    for (i = 0, cell; cell = row.cells[i]; i++) {
        if (cell == evt.target) {
            col = row.parentElement.parentElement.rows[0].cells[i].innerHTML;
            break;
        }
    }
    val = row_vals[indexToCol(i)];

    const send_post = await updateServerUrl(id, col, val, new_date_val);
    if (send_post['result'] == 'true') { 
        setRowValue(row, 'date_modified', getCurrDate())
    }
}

async function updateServerUrl(id, col, val, date_val) {
    console.log("%c updateServerUrl", "color:purple;")
    console.log({id, col, val, date_val});  
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
        console.log("%c updateServerUrl send_post", "color:purple;", send_post)
    return send_post;
}

function getCurrDate() {
    const date = new Date();
    let day = date.getDate();
    let month = date.getMonth() + 1;
    const year = date.getFullYear();
    if (String(month).length == 1) {
        month = `0${month}`
    }
    if (String(day).length == 1) {
        day = `0${day}`
    }
    return `${year}-${month}-${day}`;
}

// edit history
// UI touches
// On focus extend row
// URL dropdown
// drag rows?

// Ui touches:
// fix url dropdown
// addrow on top adds row on top
// scrollbar only available on edit
// chapters completed, average rating
// fix search bar looks
// fix add row looks
// make columns look good

// fix maxid