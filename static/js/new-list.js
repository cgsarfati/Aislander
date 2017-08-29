function displayNewList(results) {

    // results either new list name (success) or error message (try again)

    if (results === "That list already exists. Try again!") {
        // error message
        alert(results);
    } else {
        // unpack list info [name, id]
        var listName = results['list_name'];
        var listId = results['list_id'];

        var listButton = "<button type='button' class='user-list' data-list-id='" + listId + "'>" + listName + "</button>";

        $('#user-lists').append(listButton + " | ");

        // add new Div tag for that new list so that you can store
        // the grocery list of that list there.
        var DivTag = "<div class='grocery-list' id='" + listId + "' data-list-id='" + listId + "'>" + " </div>";
        $('#grocery-lists').append(DivTag);

    } // end conditional
} // end fn

function handleCreateNewList(evt) {
    evt.preventDefault();

    // package up form input values
    var formInputs = {
        "new_list_name": $("#new-list-name").val()
    };

    // send form to server, then perform success function
    $.post("/new-list.json", formInputs, displayNewList);

}

// event listener for creating new list in dashboard.html
$("#new-list").on("submit", handleCreateNewList);