function displayNewList(results) {

    // results either new list name (success) or error message (try again)

    if (results === "That list already exists. Try again!") {
        alert(results);
    } else {
        // unpack list info [name, id]
        var listName = results['list_name'];
        var listId = results['list_id'];

        // create new grocery list button
        var listButton = "<button type='button' class='btn btn-default user-list' data-list-id='" + listId + "'>" + listName + "</button>";
        $('#user-lists').append(listButton);

        // add new Div tag for that list so you can access it when
        // appending ingredients later
        var DivTag = "<div class='grocery-list' id='" + listId + "' data-list-id='" + listId + "'>" + " </div>";
        $('#grocery-lists').append(DivTag);

    } // end conditional

    // Update progress bar
    $('.progress-status').html('Step 2: Choose a grocery list');
    $("#progress-bar").attr("style", "width:25%");
} // end fn

function handleCreateNewList(evt) {
    evt.preventDefault();

    // package up info from user input
    var formInputs = {
        "new_list_name": $("#new-list-name").val()
    };

    // send info to server
    $.post("/new-list.json", formInputs, displayNewList);

}

// event listener for creating new list in dashboard.html
$("#new-list").on("submit", handleCreateNewList);