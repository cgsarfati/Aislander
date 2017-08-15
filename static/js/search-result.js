function displaySearchResults(results) {

    // get result key from json object, returns list
    var searchResults = results['results'];

    // unpack json
    for (var i = 0; i < searchResults.length; i++) {

        // format info, insert into html
        var img_url = results['baseUri'] + searchResults[i]['image'];
        var img = "<img src=" + img_url + ">" + "<br>";
        var title = "<a href='/recipe-info/" + String(searchResults[i]['id']) + "'>" + searchResults[i]['title'] + "</a>" + "<br>";
        var summary = searchResults[i]['summary'] + "<br>";

        $('#recipe').append(title + img + summary);
    }

}

function handleSearchResults(evt) {
    evt.preventDefault();

    // package up form input values
    var formInputs = {
        "recipe_search": $("#recipe-search").val(),
    };

    // send form to server, then perform success function
    $.get("/dashboard.json", formInputs, displaySearchResults);
}

// event listener for recipe search box in dashboard.html
$("#search-result").on("submit", handleSearchResults);