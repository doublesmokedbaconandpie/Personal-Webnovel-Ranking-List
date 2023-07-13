// choose column to go sort with 
document.querySelectorAll('.headcol')
        .forEach(e => e.addEventListener('click', sortRows));
document.querySelector('.headcol.col4').click();
document.querySelector('.headcol.col4').click();

function sortRows(evt) {
    const headers = evt.target.parentElement;
    const table = document.getElementById("NovelTable");
    const tableBody = table.querySelector('tbody');
    const rows = table.querySelectorAll('.dataRow');
    let newRows = Array.from(rows);

    const tmp = getMultIndexfromCol(evt.target, headers);
    const mult = tmp['mult'];
    const index = tmp['index'];
    const colName = indexToCol(index);

    newRows = mergeSort(newRows, mult, colName);
    newRows.forEach(function(row, i) {
        setRowValue(row, 'number', `${i + 1}.`);
    });

    rows.forEach(row => {
        tableBody.removeChild(row);
    });
    newRows.forEach(row => {
        tableBody.appendChild(row);
    });

    changeColClassName(evt.target);

}

function mergeSort(arr, mult, colName) {
    if (arr.length < 2) {return arr;}
    
    const middle = Math.floor(arr.length / 2);
    const left   = arr.slice(0, middle);
    const right  = arr.slice(middle, arr.length);

    return merge(mergeSort(left, mult, colName), mergeSort(right, mult, colName), mult, colName);
}

function merge(left, right, mult, colName)
{
    const result = [];
    let noSwap;
    let i = 0;
    let j = 0;

    while (i < left.length && j < right.length) {
        const cellA = getValsFromRow(left[i])[colName];
        const cellB = getValsFromRow(right[j])[colName];
        if (cellA <= cellB) {noSwap = 1 * mult;} 
        else {noSwap = -1 * mult;}

        if (cellB === "") {noSwap = -1 * mult;}
        else if (cellA === "") {noSwap = 1 * mult;}

        if (typeof(cellA) != typeof(cellB)) {
            if (typeof(cellA) === 'string') {noSwap = 1 * mult;}
            else {noSwap = -1 * mult;}
        }

        if (noSwap == 1) {
            result.push(left[i]);
            i += 1;}
        else {
            result.push(right[j]);
            j += 1;}
    }

    while (i < left.length) {
        result.push(left[i]);
        i += 1;};
    while (j < right.length) {
        result.push(right[j]);
        j += 1;};

    return result;
}

function getMultIndexfromCol(col, headers) {
    let mult;
    class_names = col.getAttribute('class');
    if (class_names.includes("sortnone") || class_names.includes("sortneg")) {mult = 1;}
    else if (class_names.includes('sortpos')) {mult = -1;}
    else {mult = 0;}

    let index;
    for (let i = 0, cell; cell = headers.cells[i]; i++) {
        if (cell == col) {
            index = i;
            break;
        }
    }

    return {'mult': mult, 'index': index};

}

function changeColClassName(col) {
    let origClass, newClass;
    class_names = col.getAttribute('class');
    if (class_names.includes('sortnone')) {
        origClass = 'sortnone';
        newClass = 'sortpos';}
    else if (class_names.includes('sortneg')) {
        origClass = 'sortneg';
        newClass = 'sortpos';}
    else if (class_names.includes('sortpos')) {
        origClass = 'sortpos';
        newClass = 'sortneg';}

    const fullClasses = class_names.replace(origClass, newClass);
    col.setAttribute('class', fullClasses);
}
