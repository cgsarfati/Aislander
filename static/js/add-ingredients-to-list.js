function DisplayUpdatedGroceryList(results) {

    // rename data that you received back from server
    var ingredientInfo = results['list_ingredients'];

    var listId = $("#list-activation-handler").val();

    for (var i = 0; i < ingredientInfo.length; i++) {
        // unpack info and place inside grocery list span tag
        var name = ingredientInfo[i]['ingredient']['name'];
        var quantity = ingredientInfo[i]['mass_qty'];
        var unit = ingredientInfo[i]['meas_unit'];

        $('div[data-list-id=' + listId + ']').append(String(quantity) + ' ' + unit + ' ' + name + '<br>');
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