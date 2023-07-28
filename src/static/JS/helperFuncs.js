export function getMaxId() {
    const div = document.getElementById("Max_Id");
    return parseInt(div.innerHTML);
}

export function setMaxId(val) {
    const div = document.getElementById("Max_Id");
    div.innerHTML = val;}

export function getValsFromRow(row) {
    let number = row.cells[0].children[0].innerHTML;
    let country = row.cells[1].children[0].innerHTML;
    let title, url;
    if (row.cells[2].children[0].querySelector("a")) {
        title = row.cells[2].children[0].children[0].innerHTML;
        url = row.cells[2].children[0].children[0].getAttribute("href");
    }
    else {
        title = row.cells[2].children[0].innerHTML;
        url = "";
    }
    let chapters_completed = row.cells[3].children[0].innerHTML;
    let rating = row.cells[4].children[0].innerHTML
    let reading_status = row.cells[5].children[0].innerHTML;
    let genre = row.cells[6].children[0].innerHTML;
    let tags = row.cells[7].children[0].innerHTML;
    let date_modified = row.cells[8].children[0].innerHTML;
    let notes = row.cells[9].children[0].innerHTML;
    let id = row.cells[10].children[0].innerHTML;

    if (parseInt(number)) {number = parseInt(number);}
    if (parseInt(rating)) {rating = parseInt(rating);}
    if (parseInt(chapters_completed)) {chapters_completed = parseInt(chapters_completed);}

    let rowVals = {'number': number,
                    'country': country,
                    'title': title,
                    'url': url,
                    'chapters_completed': chapters_completed,
                    'rating': rating,
                    'reading_status': reading_status,
                    'genre': genre,
                    'tags': tags,
                    'date_modified': date_modified,
                    'notes': notes,
                    'id': id};

    for (const column in rowVals) {
        if (rowVals[column] === "<br>") {
            rowVals[column] = "";
        }
    }

    return rowVals;
}

export function setRowValue(row, col, val) {
    const cols_to_indices = {'number': 0,
                       'country': 1,
                       'title': 2,
                       'url': 2,
                       'chapters_completed': 3,
                       'rating': 4,
                       'reading_status': 5,
                       'genre': 6,
                       'tags': 7,
                       'date_modified': 8,
                       'notes': 9,
                       'id': 10}
    const index = cols_to_indices[col];
    if (index != 2) {
        row.cells[index].children[0].innerHTML = val;
        return;
    }
    if (col == 'title') {
        row.cells[2].children[0].children[0].innerHTML = val;
        row.cells[2].children[1].children[0].innerHTML = val;
        return;
    }
    if (col == 'url') {
        row.cells[2].children[0].children[0].setAttribute("href", val);
        row.cells[2].children[1].children[0].setAttribute("href", val);
        return;
    }
    console.log('Something went wrong');
}

export function indexToCol(index) {
    const cols_to_indices = {'number': 0,
                       'country': 1,
                       'title': 2,
                       'url': 2,
                       'chapters_completed': 3,
                       'rating': 4,
                       'reading_status': 5,
                       'genre': 6,
                       'tags': 7,
                       'date_modified': 8,
                       'notes': 9,
                       'id': 10}
    return Object.keys(cols_to_indices).find(key => cols_to_indices[key] === index);
}