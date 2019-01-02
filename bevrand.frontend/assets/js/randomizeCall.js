let playlist = '';
let randomizeList = '';
let currentPlayList = 'tgif';
let currentlySelectedPlayList = '';

const config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

function changePlayList(playlistName) {
    currentPlayList = playlistName;
    for (var i = 0; i < playlist.length; i++) {
        if (playlist[i]['list'] === playlistName) {
            randomizeList = playlist[i],
            currentlySelectedPlayList = playlist[i]['displayName']
        }
        $('#currentlySelectedPlayList')
            .text(currentlySelectedPlayList);
        $('#randomizebutton')
            .text("Randomize!");
        $('#randomized_drink').hide();
    }
}

$("#randomizebutton").click(function() {

    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/api/v2/randomize`,
        data: JSON.stringify(randomizeList),
        contentType: "application/json",
        success: function(data){
            window.setTimeout(function () {
                $('#randomized_drink')
                    .text(data.result)
            });
        }
    });
});

function getAllLists () {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/v2/frontpage`,
        success: function(data){
            playlist = data;
            currentlySelectedPlayList = data[0]['displayName'];
            currentPlayList = data[0]['list'];
            randomizeList = data[0];
            $('#currentlySelectedPlayList')
                .text(currentlySelectedPlayList);
        }
    });
}

// A $( document ).ready() block.
$( document ).ready(function() {
    getAllLists();
});
