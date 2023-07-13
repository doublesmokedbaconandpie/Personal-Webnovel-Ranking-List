// choose column to go sort with 
document.querySelectorAll('.headcol')
        .forEach(e => e.addEventListener('click', sortRows));


function sortRows(evt) {
    const headers = evt.target.parentElement;
    const table = document.getElementById("NovelTable");
    const tableBody = table.querySelector('tbody');
    const rows = table.querySelectorAll('tr:not(.HeaderRow)');
    var newRows = Array.from(rows);

    var tmp = getMultIndexfromCol(evt.target, headers);
    const mult = tmp['mult'];
    const index = tmp['index'];
    const colName = indexToCol(index);

    newRows = mergeSort(newRows, mult, colName);
    newRows.forEach(function(row, i) {
        setRowValue(row, 'number', `${i + 1}.`)
    })

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
    
    var middle = Math.floor(arr.length / 2);
    var left   = arr.slice(0, middle);
    var right  = arr.slice(middle, arr.length);

    return merge(mergeSort(left, mult, colName), mergeSort(right, mult, colName), mult, colName);
}

function merge(left, right, mult, colName)
{
    var result = [];
    var noSwap;
    var i = 0;
    var j = 0;

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
    var mult;
    class_names = col.getAttribute('class');
    if (class_names.includes("sortnone") || class_names.includes("sortneg")) {mult = 1;}
    else if (class_names.includes('sortpos')) {mult = -1;}
    else {mult = 0;}

    var index;
    for (let i = 0, cell; cell = headers.cells[i]; i++) {
        if (cell == col) {
            index = i;
            break;
        }
    }

    return {'mult': mult, 'index': index};

}

function changeColClassName(col) {
    var origClass, newClass;
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

    var fullClasses = class_names.replace(origClass, newClass);
    col.setAttribute('class', fullClasses);
}
