document.querySelectorAll('.deleteRow')
        .forEach(e => e.addEventListener('click', deleteRowbutton));

async function deleteRowbutton(evt) {
    var row = evt.target.parentElement.parentElement.parentElement;
    const tablebody = row.parentElement
    tablebody.removeChild(row);
    result = await updateServerDeleteRow(row);
}

async function updateServerDeleteRow(row) {
    var id = getValsFromRow(row)['id'];
    const send_post = await fetch(`/deleteRow`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            id: id
            })
        })
        .then(response => response.json());

    console.log("%c updateServerDeleteRow", "color:red;")
    console.log({id, send_post});  
    return send_post;
}