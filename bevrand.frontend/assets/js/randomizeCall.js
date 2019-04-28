var playlist = [];
var randomizeList = '';
var currentPlayList = 'tgif';
var currentlySelectedPlayList = '';

var token = "";
var username = "";

var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    token = localStorage.getItem("jwt");
    if (token) {
        var jwtDecoded = parseJwt(token);
        username = jwtDecoded['username'];
        getUserPlaylist(function(userPlaylists) {
            if (userPlaylists.length === 0) {
                var playlistHtml = "<article>"
                    + '<header>'
                    + '<h3><a class="scrolly" href="/profile.html">You do not have any playlists! Create one in your Profile</a></h3>'
                    + '</header >'
                    + '</article >'

                $('.reel').append(playlistHtml);
            }
            $('#navlinkLogin').hide();
            $('#navlinkRegister').hide();
            $('#navlinkLogout').show();
            $('#navlinkProfile').show();
            setGlobalVariables(userPlaylists['result']);
            appendPlaylistsToCarrousel(userPlaylists['result']);
        });
    }
    else {
        getAllLists(function (playlists) {
            $('#navlinkLogin').show();
            $('#navlinkRegister').show();
            $('#navlinkLogout').hide();
            $('#navlinkProfile').hide();
            setGlobalVariables(playlists);
            appendPlaylistsToCarrousel(playlists);
        });
    }
});

$("#navlinkLogout").click(function () {
    localStorage.setItem("jwt", "");

    $('.reel').html("");

    getAllLists(function (playlists) {
        $('#randomizebutton')
            .text("Randomize!");
        $('#randomizedDrink').hide();

        $('#navlinkLogin').show();
        $('#navlinkRegister').show();
        $('#navlinkLogout').hide();
        $('#navlinkProfile').hide();
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
    $('#navbar').hide();
    if (token) {
        $.ajax({
            type: "POST",
            headers: {"x-api-token": token },
            url: `${config.proxyHostname}/randomize-api/v1/randomize`,
            data: JSON.stringify(randomizeList),
            contentType: "application/json",
            success: function (data) {
                window.setTimeout(function () {
                    $('#randomizedDrink')
                        .text(data.result)
                })
            },
            error: function () {
                window.setTimeout(function () {
                    $('#randomizedDrink')
                        .text("Could not get a drink, we are sorry :(")
                });
            }
        })
    }
    else {
    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/randomize-api/v2/randomize`,
        data: JSON.stringify(randomizeList),
        contentType: "application/json",
        success: function (data) {
            window.setTimeout(function () {
                $('#randomizedDrink')
                    .text(data.result)
            })
        },
        error: function () {
            window.setTimeout(function () {
                $('#randomizedDrink')
                    .text("Could not get a drink, we are sorry :(")
            });
        }
    })}
});

function getAllLists(callback) {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/playlist-api/v2/frontpage`,
        success: function (data) {
            callback(data);
        }
    });
}

function getUserPlaylist(callback) {
    $.ajax({
        type: "GET",
        headers: {"x-api-token": token },
        url: `${config.proxyHostname}/playlist-api/v1/private/${username}`,
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
    return "<article>"
        + '<a class="image featured scrolly" onclick=changePlayList("' + playlist.list + '") href="#main"><img src="' + playlist.imageUrl + '" /></a>'
        + '<header>'
        + '<h3><a class="scrolly" onclick=changePlayList("' + playlist.list + '") href="#main">' + playlist.displayName + '</a></h3>'
        + '</header >'
        + '<ul style="list-style-type:none">' + itemList + '</ul>'
        + '</article >'
}

