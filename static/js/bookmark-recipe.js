function printBookmarkSuccess(results) {

    // results either success or error message

    if (results === "You've already bookmarked this recipe.") {
        // error message
        alert(results);
    } else {
        // success message
        alert(results);
    } // end conditional
} // end fn

function handleBookmarkRecipe(evt) {

    // package up info
    // "this" - keyword that refers to THIS button (since each recipe has its own button)
    // recipeId inside .data refers to data-recipe-id attribute in button tag
    var recipeId = $(this).data("recipeId");

    // send info to server; if successful, execute function
    $.post('/bookmark.json', {'recipe_id': recipeId}, printBookmarkSuccess);

}

// event listener for bookmark button
// use document vs. element identifier
$(document).on('click', '.favorite', handleBookmarkRecipe);