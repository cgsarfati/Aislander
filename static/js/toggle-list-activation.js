function changeListStatus(evt) {

    // get list id of button you clicked
    var listId = $(this).data("listId");

    // change value to button's list_id 
    $("#list-activation-handler").val(listId);


} // end fn

$(document).on('click', '.user-list', changeListStatus);