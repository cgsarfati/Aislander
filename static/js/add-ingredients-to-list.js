function DisplayUpdatedGroceryList(results) {

    // rename data that you received back from server
    var ingredientInfo = results['list_ingredients'];

    // get listId so you can target specific grocery list div tag
    var listId = $("#list-activation-handler").val();

    // create list of existing list-aisle ids represented as ul ids
    var existingAisleIds = [];

    $('.grocery-list[data-list-id=' + listId + '] ul').each(function () {
        existingAisleIds.push(this.id);
    });

    // loop through ingredients and append <li> ingredient to aisle
    for (var i = 0; i < ingredientInfo.length; i++) {
        var ingredientAisleId = ingredientInfo[i]['ingredient']['aisle_id'];
        var ingredientAisleName = ingredientInfo[i]['ingredient']['aisle_name'];

        // if <ul> aisle doesn't exist, add new <ul> aisle
        if (existingAisleIds.indexOf(listId + "-" + ingredientAisleId) === -1) {
            var newAisle = $("<ul>");
            newAisle.attr("id", listId + "-" + ingredientAisleId);
            newAisle.append(ingredientAisleName);
            $('#' + listId).append(newAisle);
            existingAisleIds.push(listId + "-" + ingredientAisleId);
        }

        // At this point, aisle exists. Create new <li> tag for each ingredient
        // and append it to <ul> aisle.
        var newItem = $("<li>");

        var name = ingredientInfo[i]['ingredient']['name'];
        var quantity = ingredientInfo[i]['mass_qty'] + " "; // integer
        var unit = ingredientInfo[i]['meas_unit'] + " ";

        newItem.append(String(quantity) + unit + name);

        $("#" + listId + "-" + ingredientAisleId).append(newItem);

    } // end loop

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