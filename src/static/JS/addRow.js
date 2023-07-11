var Max_ID = getMaxId();

document.getElementById("addRow")
        .addEventListener("click", addRowClick);

function addRowClick() {
    const table = document.getElementById("NovelTable");
    if (checkLastRowEmpty(table)) {return;}
    row = table.insertRow(table.rows.length);
    for (let i = 0; i < table.rows[0].cells.length; i++) {
        if (i == 0) {
            createCell(row.insertCell(i), `${table.rows.length - 1}.`, 'col0', false);
            continue;}
        if (i == 2) {
            createCellTitleUrl(row.insertCell(i));
            continue;}
        if (i == 8) {
            createCell(row.insertCell(i), "", 'col8', false);
            continue;}
        if (i == 10) {
            createCell(row.insertCell(i), Max_ID + 1, 'col10', false);
            Max_ID += 1;
            continue;}
        if (i == 11) {
            createCellDelete(row.insertCell(i));
            Max_ID += 1;
            continue;}
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
    cell.addEventListener('blur', saveEditCell);
    return cell;
}

function createCellTitleUrl(cell) {
    var div1 = document.createElement('div');
    var txt1 = document.createElement('a');
    txt1.setAttribute('href', '');
    div1.appendChild(txt1);
    div1.setAttribute('class', "scrollable");
    div1.setAttribute("contenteditable", "true");

    var div2 = document.createElement('div');
    var txt2 = document.createElement('a');
    txt2.setAttribute('href', '');
    div2.appendChild(txt2);
    div2.setAttribute('class', "col2dropdown");

    cell.setAttribute("class", "col2");
    cell.appendChild(div1);
    cell.appendChild(div2);
    cell.addEventListener('keydown', keydownListener);
    cell.addEventListener('blur', saveEditCell);
    return cell;
}

function createCellDelete(cell) {
    var div = document.createElement('div');
    var button = document.createElement('button');
    button.setAttribute('class', 'deleteRow');
    button.innerHTML = 'Delete Row';
    div.appendChild(button);

    cell.setAttribute("class", "col11");
    cell.appendChild(div);
    return cell;
}

function checkLastRowEmpty(table){
    var last_row = table.rows[table.rows.length - 1];
    RowData = getValsFromRow(last_row);
    for (const [key, value] of Object.entries(RowData)) {
        if (key == 'id' || key == 'number') {continue;}
        if (value != '') {return false;}
    }
    return true;
}

function getMaxId() {
    const table = document.getElementById("NovelTable");
    let last_row = table.rows[table.rows.length - 1];
    return parseInt(getValsFromRow(last_row)['id']);
}