
function getValsFromRow(row) {
    number = row.cells[0].children[0].innerHTML;
    country = row.cells[1].children[0].innerHTML;
    title = row.cells[2].children[0].children[0].innerHTML;
    url = row.cells[2].children[0].children[0].getAttribute("href");
    chapters_completed = row.cells[3].children[0].innerHTML;
    rating = row.cells[4].children[0].innerHTML
    reading_status = row.cells[5].children[0].innerHTML;
    genre = row.cells[6].children[0].innerHTML;
    tags = row.cells[7].children[0].innerHTML;
    date_modified = row.cells[8].children[0].innerHTML;
    notes = row.cells[9].children[0].innerHTML;
    id = row.cells[10].children[0].innerHTML;

    number = parseInt(number);

    return {'number': number,
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
}

function setRowValue(row, col, val) {
    cols_to_indices = {'number': 0,
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
    console.log(col in cols_to_indices, col);
    index = cols_to_indices[col];
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

function indexToCol(index) {
    cols_to_indices = {'number': 0,
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