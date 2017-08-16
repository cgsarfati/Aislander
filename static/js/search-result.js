function displaySearchResults(results) {

    // get result key from json object, returns list
    var searchResults = results['results'];

    // unpack json
    for (var i = 0; i < searchResults.length; i++) {

        // format info into elements

        var beginDiv = "<div class='recipe'>";
        var endDiv = "</div>";

        var imgUrl = results['baseUri'] + searchResults[i]['image'];
        var img = "<img src=" + imgUrl + ">" + "<br>";

        var recipeId = String(searchResults[i]['id']);

        var title = "<a href='/recipe-info/" + recipeId + "'>" +
                     searchResults[i]['title'] + "</a>";

        var summary = searchResults[i]['summary'] + "<br>";

        var bookmarkButton = "<button type='button' class='favorite' data-recipe-id='" + recipeId + "'>Bookmark</button>";
        var addButton = "<button type='button' class='addRecipe' data-recipe-id='" + recipeId + "'>Add Recipe</button> </br>";
        
        // add all elements together; each recipe will have its own div
        $('#recipes').append(beginDiv + title + bookmarkButton + addButton + img + summary + endDiv);
    }

}

function handleSearchResults(evt) {
    evt.preventDefault();

    // package up form input values
    var formInputs = {
        "recipe_search": $("#recipe-search").val(),
    };

    // send form to server, then perform success function
    $.get("/search.json", formInputs, displaySearchResults);
}

// event listener for recipe search box in dashboard.html
$("#search-result").on("submit", handleSearchResults);