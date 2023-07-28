import { getValsFromRow, setRowValue, indexToCol } from "./helperFuncs.js";

export function findListener(evt){
    if (evt.key === "Enter" || evt.key == 'Escape') {
        evt.target.blur();
    }
}

export function findEntries(evt) {
    console.log("Find Entries");
    const search_query = evt.target.innerHTML.toLowerCase();
    const search_index = getFindColIndex(evt.target);
    const col_name = indexToCol(search_index);
    const rows = Array.from(document.querySelectorAll('.dataRow'));
    const foundRows = [];

    rows.forEach(function(row) {
        let innerVal = String(getValsFromRow(row)[col_name]).toLowerCase();
        if (!innerVal.includes(search_query)) {            
            row.classList.add(`notFound${search_index}`);}
        else {row.classList.remove(`notFound${search_index}`);}
        if (!row.getAttribute("class").includes("notFound")) {
            foundRows.push(row);}
    });

    foundRows.forEach(function(row, i) {
        setRowValue(row, 'number', `${i + 1}.`);
    });
}

function getFindColIndex(target) {
    const targetClass = target.getAttribute("class");
    return parseInt(targetClass.replace("col", ""));
}