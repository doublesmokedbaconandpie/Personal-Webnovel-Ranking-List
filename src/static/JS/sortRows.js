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

    while (left.length && right.length) {
        const cellA = getValsFromRow(left[0])[colName];
        const cellB = getValsFromRow(right[0])[colName];
        if (cellA <= cellB) {noSwap = 1 * mult;} 
        else {noSwap = -1 * mult;}

        if (cellB === "") {noSwap = -1 * mult;}
        else if (cellA === "") {noSwap = 1 * mult;}

        if (typeof(cellA) != typeof(cellB)) {
            if (typeof(cellA) === 'string') {noSwap = 1 * mult;}
            else {noSwap = -1 * mult;}
        }

        console.log(cellA, cellB, cellA <= cellB, cellB < cellA, noSwap, mult)

        if (noSwap == 1) {
            result.push(left.shift());}
        else {result.push(right.shift());}
    }

    while (left.length) {result.push(left.shift())};
    while (right.length) {result.push(right.shift())};

    return result;
}

function getMultIndexfromCol(col, headers) {
    var mult;
    class_names = col.getAttribute('class');
    console.log(class_names);
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
