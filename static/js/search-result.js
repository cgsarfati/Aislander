function displaySearchResults(results) {

    // gest result key from json object, returns list
    var searchResults = results['results'];

    // unpack json into readable format and insert into dashboard.html
    for (var i = 0; i < searchResults.length; i++) {
        $('#recipe-title').html(searchResults[i]['title']);
        $('#recipe-pic').attr("src", searchResults[i]['image']);
    }
}

function getSearchResults(evt) {
    evt.preventDefault();

    // retrieve form input values
    var formInputs = {
        "recipe_search": $("#recipe-search").val(),
    };

    // get json response from server.py, then perform success function
    $.get("/dashboard.json", formInputs, displaySearchResults);
}

// event listener for recipe search box in dashboard.html
$("#search-result").on("submit", getSearchResults);