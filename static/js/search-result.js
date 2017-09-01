function displaySearchResults(results) {

    // get result key from json object, returns list
    var searchResults = results['results'];

    // unpack list, accessing necessary info
    for (var i = 0; i < searchResults.length; i++) {

        // create div tag to serve as container for each recipe
        var beginDiv = "<div class='recipe'>";
        var endDiv = "</div>";

        // create img
        var imgUrl = results['baseUri'] + searchResults[i]['image'];
        var img = "<img src=" + imgUrl + ">" + "<br>";

        // create recipe title (as a link)
        var recipeId = String(searchResults[i]['id']);

        var title = "<a href='/recipe-info/" + recipeId + "'>" +
                     searchResults[i]['title'] + "</a>";

        // create summary
        var summary = searchResults[i]['summary'] + "<br>";

        // beside each recipe title, add two buttons: 'bookmark' and 'add to list'
        var bookmarkButton = "<button type='button' class='favorite' data-recipe-id='" + recipeId + "'>Bookmark</button>";
        var addButton = "<button type='button' class='add-to-list' data-recipe-id='" + recipeId + "'>Add To List</button> </br>";
        
        // add all elements together into recipe div element
        $('#recipes').append(beginDiv + title + bookmarkButton + addButton + img + summary + endDiv);
    } // end loop

} // end fn

function handleSearchResults(evt) {
    evt.preventDefault();

    // package up info from user input
    var formInputs = {
        "recipe_search": $("#recipe-search").val(),
        "number_of_results": $("#search-quantity").val(),
    };

    // send info to server
    $.get("/search.json", formInputs, displaySearchResults);
}

// event listener for recipe search box in dashboard.html
$("#search-result").on("submit", handleSearchResults);