let playlist = '';
let currentPlayList = 'tgif';

const config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$("#randomizebutton").click(function() {

    let randomizeList = '';

    for (var i = 0; i < playlist.length; i++) {
        if (playlist[i]['list'] === currentPlayList) {
            randomizeList = playlist[i]
        }
    }

    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/api/v2/randomize`,
        data: JSON.stringify(randomizeList),
        contentType: "application/json",
        success: function(data){
            window.setTimeout(function () {
                $('#randomized_drink')
                    .text(data.result)
                    .show()
            }, 4500);
        }
    });
});

function getAllLists () {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/v2/frontpage`,
        success: function(data){
            playlist = data;
        }
    });
}

// A $( document ).ready() block.
$( document ).ready(function() {
    getAllLists();
});
