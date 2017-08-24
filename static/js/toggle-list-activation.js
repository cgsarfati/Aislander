function changeListStatus(evt) {

    // get list id of button you clicked
    var listId = $(this).data("listId");

    // change value to button's list_id 
    $("#list-activation-handler").val(listId);

    // access div tags of grocery list, and set all to hide initially
    // then isolate div tag of that particular list
    $(".grocery-list").hide();

    $('div[data-list-id=' + listId + ']').show();

} // end fn

// event listener for isolating lists
$(document).on('click', '.user-list', changeListStatus);