let drink = '';
let playlist = '';

function randomizeThatShit () {
    getAllLists().done(handleData);
    console.log(playlist);
    let local = playlist[0]
    $.ajax({
        type: "POST",
        url: "http://localhost:4540/api/v2/randomize",
        data: { local },
        success: function(data){
            console.log(data);
        }
    });
}

function getAllLists () {
     return $.ajax({
        type: "GET",
        url: "http://localhost:4540/api/v2/frontpage"
    });
}

function handleData(data /* , textStatus, jqXHR */ ) {
    playlist = data;
    //do some stuff
}

// A $( document ).ready() block.
$( document ).ready(function() {
    randomizeThatShit();
});
