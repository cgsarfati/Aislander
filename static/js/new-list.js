function displayNewList(results) {

    // results either new list name (success) or error message (try again)

    if (results === "That list already exists. Try again!") {
        // error message
        alert(results);
    } else {
        // rename, show list
        var new_list_name = results;
        $('#lists').append(new_list_name + ' | ');
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

} // end fn


// event listener for creating new list in dashboard.html
$("#new-list").on("submit", handleCreateNewList);