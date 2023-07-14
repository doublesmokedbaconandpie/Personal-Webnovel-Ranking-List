
document.querySelectorAll('.find')
        .forEach(e => e.addEventListener('blur', findEntries));


function findEntries(evt) {
    console.log(evt);
}