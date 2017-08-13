function displayRecipeSummaries(results) {

    // unpack list of jsons
    // retrieve summary keys of objects
    // insert values of those keys into recipe-summary div

} // end fn

function displaySearchResults(results) {

    // get result key from json object, returns list
    var searchResults = results['results'];

    // store ids to be packaged up
    var recipe_ids = {
        "recipe_id": []
    };

    // unpack json
    for (var i = 0; i < searchResults.length; i++) {

        // format info, insert into html
        var img_url = results['baseUri'] + searchResults[i]['image'];
        var title = searchResults[i]['title'] + "<br>";
        var img = "<img src=" + img_url + ">" + "<br>";
        $('#recipe-title-img').append(title + img);

        // append ids into object
        var recipe_id = searchResults[i]['id'];
        recipe_ids["recipe_id"].push(recipe_id);
    }

    // send ids to server, then perform success function
    $.get("/recipe-summaries.json", recipe_ids, displayRecipeSummaries);

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