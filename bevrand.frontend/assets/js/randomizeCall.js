var playlist = [];
var randomizeList = '';
var currentPlayList = 'tgif';
var currentlySelectedPlayList = '';

var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    getAllLists(function (playlists) {
        setGlobalVariables(playlists);
        appendPlaylistsToCarrousel(playlists);
    });
});

function changePlayList(playlistName) {
    currentPlayList = playlistName;
    for (var i = 0; i < playlist.length; i++) {
        if (playlist[i]['list'] === playlistName) {
            randomizeList = playlist[i]
                currentlySelectedPlayList = playlist[i]['displayName']
        }
        $('#currentlySelectedPlayList')
            .text(currentlySelectedPlayList);
        $('#randomizebutton')
            .text("Randomize!");
        $('#randomizedDrink').hide();
    }
}

$("#randomizebutton").click(function () {
    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/api/v2/randomize`,
        data: JSON.stringify(randomizeList),
        contentType: "application/json",
        success: function (data) {
            window.setTimeout(function () {
                $('#randomizedDrink')
                    .text(data.result)
            });
        }
    });
});

function getAllLists(callback) {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/v2/frontpage`,
        success: function (data) {
            callback(data);
        }
    });
}

function setGlobalVariables(data) {
    playlist = data;
    currentlySelectedPlayList = data[0]['displayName'];
    currentPlayList = data[0]['list'];
    randomizeList = data[0];
    $('#currentlySelectedPlayList')
        .text(currentlySelectedPlayList);
}

function appendPlaylistsToCarrousel(playlists = []) {
    for (var i = 0; i < playlists.length; i++) {
        var playlist = playlists[i];
        var playlistHtml = generatePlaylistHtml(playlist);
        $('.reel').append(playlistHtml);
    }
}

function generatePlaylistHtml(playlist) {
    var itemList = playlist.beverages.reduce(function (htmlList, beverage) {
        return htmlList + "<li>" + beverage + "</li>";
    }, "");
    var playlistHtml = "<article>"
        + '<a class="image featured scrolly" onclick=changePlayList("' + playlist.list + '") href="#main"><img src="' + playlist.imageUrl + '" /></a>'
        + '<header>'
        + '<h3><a class="scrolly" onclick=changePlayList("' + playlist.list + '") href="#main">' + playlist.displayName + '</a></h3>'
        + '</header >'
        + '<ul style="list-style-type:none">' + itemList + '</ul>'
        + '</article >'
    return playlistHtml;
}
// A $( document ).ready() block.

