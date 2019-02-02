
var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    $('#playListCreationField').hide();
    $('#okPlayListCreation').hide();
    $('#cancelPlayListCreation').hide();
    getPersonalPlaylists("joost", function (playlists) {
        appendPlaylistToWorkspace(playlists);
    });
});

function appendPlaylistToWorkspace(playlists = []) {
    for (var i = 0; i < playlists.length; i++) {
        var playlist = playlists[i];
        var playlistHtml = addPlaylistsToPersonalSpace(playlist);
        console.log(playlistHtml)
        $('#personalPlaylists').append(playlistHtml);


        var coll = document.getElementsByClassName("collapsible");
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
}

function addPlaylistsToPersonalSpace(playlist) {
    var itemList = playlist.beverages.reduce(function (htmlList, beverage) {
        return htmlList + "<li>" + beverage + "</li>";
    }, "");
    var playlistHtml = '<li>'
        + '<button class="collapsible" >' + playlist.displayName + ' <i class="fa fa-pencil"></i> <i class="fa fa-trash"></i></button>'
        + '<div class="contentpersonalplaylist"><ul style="list-style-type:none">' + itemList + '</ul> </div>'
        + '</li>'

    return playlistHtml;
}

function getPersonalPlaylists(username, callback) {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/playlists?username=${username}`,
        success: function (data) {
            callback(data);
        }
    });
}

function getPersonalPlaylist(username, playlistname, callback) {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/playlists?username=${username}&list=${playlistname}`,
        success: function (data) {
            console.log(data)
            callback(data);
        },
        error: function () {
            callback(true)
        }
    });
}

function addNewPlayList() {
    $('#playListCreationField').show();
    $('#okPlayListCreation').show();
    $('#cancelPlayListCreation').show();
}

$("#cancelPlayListCreation").click(function () {
    $('#playListCreationField').hide();
    $('#okPlayListCreation').hide();
    $('#cancelPlayListCreation').hide();
});

$("#okPlayListCreation").click(function () {
    var normalizedName = document.getElementById("playListCreationField").value.replace(/[^a-zA-Z0-9]/g, "").toLowerCase();
    getPersonalPlaylist("joost", normalizedName, function (playlist) {
        var nameIsNewList = true;
        for (var i = 0; i < playlist.length; i++) {
            if (playlist[i]['list'] === normalizedName) {
                nameIsNewList = false;
            }
        }
         console.log(nameIsNewList)
        if (nameIsNewList)  {
            window.location.href = 'playlistcreation.html';
        }
    })

});

