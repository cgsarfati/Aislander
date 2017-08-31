function printBookmarkStatus(results) {

    // results is either success or error message

    if (results === "You've already bookmarked this recipe.") {
        // error message
        alert(results);
    } else {
        // success message
        alert(results);
    }
}

function handleBookmarkRecipe(evt) {

    // extract recipe id from data attribute, package it up to be sent to server
    // "this" - keyword that refers to THIS bookmark button (since each 
    // recipe has the same button).
    var recipeId = $(this).data("recipeId");

    // send info to server; if successful, execute function
    $.post('/bookmark.json', {'recipe_id': recipeId}, printBookmarkStatus);

}

// event listener for bookmark button in dashboard.html

// use document vs. element identifier, since there are many bookmark buttons
// in the same page. only unique identifier of button is data attribute,
// which will be used later.
$(document).on('click', '.favorite', handleBookmarkRecipe);