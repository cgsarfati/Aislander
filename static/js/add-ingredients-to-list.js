function DisplayUpdatedGroceryList(results) {

    // unpack info and place inside grocery list span tag
    var ingredientNames = results['ing_name'];

    var listId = $("#list-activation-handler").val();

    for (var i = 0; i < ingredientNames.length; i++) {
        $('div[data-list-id=' + listId + ']').append(ingredientNames[i]);
    }

} // end fn

function handleAddIngredientsToList(evt) {

    // package up relevant info to send to server to add to DB
    var listIngredientsData = {'recipeId': $(this).data("recipeId"),
                    'listId': $("#list-activation-handler").val()
    };

    // send to server; if successful, execute function
    $.post('/add-to-list.json', listIngredientsData, DisplayUpdatedGroceryList);

} // end fn

$(document).on('click', '.add-to-list', handleAddIngredientsToList);