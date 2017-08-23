function DisplayUpdatedGroceryList(results) {

} // end fn

function handleAddIngredientsTolist(evt) {

    // package up relevant info to send to server to add to DB
    var listIngredientsData = {'recipeId': $(this).data("recipeId"),
                    'listId': $("#list-activation-handler").val()
    };

    // send server; if successful, execute function
    $.post('/add-to-list.json', listIngredientsData, DisplayUpdatedGroceryList);

} // end fn

$(document).on('click', '.add-to-list', handleAddIngredientsToList);