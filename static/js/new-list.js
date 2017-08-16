function displayNewList(results) {

    // rename returned data
    var newlistName = results;

    // alert user that recipe is bookmarked
    alert(newlistName + "has been added as a new list!");

} // end fn

function handleCreateNewList(evt) {
    evt.preventDefault();

    // package up form input values
    var formInputs = {
        "new_list_name": $("#new-list-name").val(),
    };

    // send form to server, then perform success function
    $.post("/grocery-list.json", formInputs, displayNewList);

} // end fn


// event listener for creating new list in dashboard.html
$("#new-list").on("submit", handleCreateNewList);