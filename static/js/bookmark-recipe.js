function printBookmarkSuccess(results) {

    // alert user that recipe is bookmarked
    alert(results + " has been bookmarked!");
}

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