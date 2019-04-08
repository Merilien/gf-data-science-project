function getTitles(movies) {
    var titles = Object.values(movies);
    return titles;
}

function getKeys(movies) {
    var ids = Object.keys(movies);
    return ids;
}

function setTypeAhead(movies) {
    var input = $('#add');
    var titles = getTitles(movies)
    input.typeahead({
        source: titles,
        limit: 10,
        minLength: 2
    });
}


