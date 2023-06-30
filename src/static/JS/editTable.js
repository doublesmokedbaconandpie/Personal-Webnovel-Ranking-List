
var addRow = document.getElementById("addRow");
addRow.addEventListener("click", addRowClick);

function addRowClick() {
    var table = document.getElementById("NovelTable");
    if (checkLastRowEmpty(table)) {return;}
    row = table.insertRow(table.rows.length);
    for (let i = 0; i < table.rows[0].cells.length; i++) {
        if (i == 0) {
            createCell(row.insertCell(i), `${table.rows.length - 1}.`, 'col0', false);
            continue;
        }
        if (i == 2) {
            createCell(row.insertCell(i), "", 'col2', false);
            let div1 = row.cells[2].childNodes[0];
            div1.setAttribute("contenteditable", true);
            continue;
        }
        if (i == 8) {
            createCell(row.insertCell(i), "", 'col8', false);
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
    
    if (content_editable) {
        cell.setAttribute("contenteditable", "true");
    }
    cell.setAttribute("class", class_name)
    cell.appendChild(div);
}

function checkLastRowEmpty(table){
    var last_row = table.rows[table.rows.length - 1];
    for (let i = 1; i < last_row.cells.length; i++) {
        let inner_div = last_row.cells[i].childNodes[0];
        if (inner_div.innerHTML != "") {
            return false;
        }
    }
    return true;
}