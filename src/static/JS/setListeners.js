import { addRowClick } from "./addRow.js";
import { deleteRowbutton } from "./deleteRow.js";
import { saveEditCell, cellKeyDown, titleEditor, titleKeyDown} from "./editCell.js";
import { findEntries, findListener } from "./findRows.js";
import { sortRows } from "./sortRows.js";

document.querySelectorAll(".addRow")
        .forEach(e => e.addEventListener('click', addRowClick));

document.querySelectorAll('.deleteRow')
        .forEach(e => e.addEventListener('click', deleteRowbutton));

document.querySelectorAll('#NovelTable td')
        .forEach(e => e.addEventListener('blur', saveEditCell));
document.querySelectorAll('#NovelTable td')
        .forEach(e => e.addEventListener('keydown', cellKeyDown));
document.querySelectorAll('#NovelTable td div')
        .forEach(e => e.addEventListener('blur', titleEditor));
document.querySelectorAll('#NovelTable td div')
        .forEach(e => e.addEventListener('keydown', titleKeyDown));


document.querySelectorAll('#FindRow td')
        .forEach(e => e.addEventListener('blur', findEntries));
document.querySelectorAll('#FindRow td')
        .forEach(e => e.addEventListener('keydown', findListener));

document.querySelectorAll('.headcol')
        .forEach(e => e.addEventListener('click', sortRows));
document.querySelector('.headcol.col4').click();