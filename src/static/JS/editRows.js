const table = document.getElementById("NovelTable");
var Max_ID = getMaxId();

document.getElementById("addRow")
        .addEventListener("click", addRowClick);

function addRowClick() {
    if (checkLastRowEmpty(table)) {return;}
    row = table.insertRow(table.rows.length);
    for (let i = 0; i < table.rows[0].cells.length; i++) {
        if (i == 0) {
            createCell(row.insertCell(i), `${table.rows.length - 1}.`, 'col0', false);
            continue;}
        if (i == 2) {
            createCell(row.insertCell(i), "", 'col2', false);
            let div1 = row.cells[2].children[0];
            div1.setAttribute("contenteditable", true);
            continue;}
        if (i == 8) {
            createCell(row.insertCell(i), "", 'col8', false);
            continue;}
        if (i == 10) {
            createCell(row.insertCell(i), Max_ID + 1, 'col10', false);
            Max_ID += 1;
            continue;
        }
        createCell(row.insertCell(i), "", `col${i}`, true);
    }
}    

function createCell(cell, text, class_name, content_editable) {
    var div = document.createElement('div');
    var txt = document.createTextNode(text);
    div.appendChild(txt);
    div.setAttribute('class', "scrollable");
    
    if (content_editable) {cell.setAttribute("contenteditable", "true");}
    cell.setAttribute("class", class_name);
    cell.appendChild(div);
    cell.addEventListener('keydown', keydownListener);
    cell.addEventListener('blur', editCell);
}

function checkLastRowEmpty(table){
    var last_row = table.rows[table.rows.length - 1];
    for (let i = 1; i < 10; i++) {
        let inner_div = last_row.cells[i].children[0];
        if (inner_div.innerHTML != "") {
            return false;
        }
    }
    return true;
}

function getMaxId() {
    let last_row = table.rows[table.rows.length - 1];
    return parseInt(last_row.cells[10].children[0].innerHTML);
}