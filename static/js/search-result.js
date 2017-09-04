function displaySearchResults(results) {

    $("#recipes").empty();

    // get result key from json object, returns list
    var searchResults = results['results'];

    // unpack list, accessing necessary info
    for (var i = 0; i < searchResults.length; i++) {

        // create div tag to serve as container for each recipe
        var beginDiv = "<div class='recipe text-center'>";
        var endDiv = "</div>";

        // create img
        var imgUrl = results['baseUri'] + searchResults[i]['image'];
        var img = "<img src=" + imgUrl + " class='img-rounded'>" + "<br>";

        // create recipe title (as a link)
        var recipeId = String(searchResults[i]['id']);

        var title = "<h3 class='recipe-title' data-recipe-id='" + recipeId + "'> <a href='/recipe-info/" + recipeId + "'>" +
                     searchResults[i]['title'] + "</a> </h3>";

        // create summary
        var summary = "<p>" + searchResults[i]['summary'] + "</p> <br>";

        // beside each recipe title, add two buttons: 'bookmark' and 'add to list'
        var bookmarkButton = "<button type='button' class='favorite' data-recipe-id='" + recipeId + "'> <span class='glyphicon glyphicon-heart'></span> </button>";
        var addButton = "<button type='button' class='add-to-list' data-recipe-id='" + recipeId + "'> <span class='glyphicon glyphicon-shopping-cart'></span> </button> </br>";
        
        // add all elements together into recipe div element
        $('#recipes').append(beginDiv + title + bookmarkButton + addButton + img + summary + endDiv);
    } // end loop

    // Update progress bar
    $('.progress-status').html('Step 4: Click the shopping cart icon to add ingredients to your list!');
    $("#progress-bar").attr("style", "width:75%");

} // end fn

function handleSearchResults(evt) {
    $("#recipes").html("<button class='buttonload'><i class='fa fa-spinner fa-spin'></i> Looking for recipes...</button>");

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