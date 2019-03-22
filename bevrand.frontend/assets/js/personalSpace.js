var username = '';
var token = '';

var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    token = localStorage.getItem("jwt");
    var jwtDecoded = parseJwt(token);
    username = jwtDecoded['username'];

    $('#personalSpaceUsername')
        .text(username + "'s personal workspace");
    $('#playListCreationField').hide();
    $('#okPlayListCreation').hide();
    $('#cancelPlayListCreation').hide();
    getPersonalPlaylists(username, function (playlists) {
        appendPlaylistToWorkspace(playlists);
    });
    getUserInfo(username, function (userInfo) {
        $('#emailAddressPersonal')
            .text(`Email: ${userInfo.emailAddress}`);
        $('#usernamePersonal')
            .text(`Username: ${userInfo.username}`);
    });
    localStorage.setItem("username", username);
});

function appendPlaylistToWorkspace(playlists = []) {
    for (var i = 0; i < playlists.length; i++) {
        var playlist = playlists[i];
        var playlistHtml = addPlaylistsToPersonalSpace(playlist);
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
    return '<li>'
        + '<button class="collapsible" >' + playlist.displayName + '  <i style="margin-left: 0.5em" class="fa fa-pencil"></i> <i style="margin-left: 0.5em" class="fa fa-trash"></i></button>'
        + '<div class="contentpersonalplaylist"><ul style="list-style-type:none">' + itemList + '</ul> </div>'
        + '</li>'
}

function getPersonalPlaylists(username, callback) {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/playlists?username=${username}`,
        success: callback
    });
}

function getUserInfo(username, callback) {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/Users?by-username=${username}`,
        success: callback
    });
}

function getPersonalPlaylist(username, playlistname, callback) {
    $.ajax({
        type: "GET",
        url: `${config.proxyHostname}/api/playlists?username=${username}&list=${playlistname}`,
        success: callback
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
    var displayName = document.getElementById("playListCreationField").value;
    var normalizedName = document.getElementById("playListCreationField").value
        .replace(/[^a-zA-Z0-9]/g, "")
        .toLowerCase();
    getPersonalPlaylist(username, normalizedName, function (playlist) {
        var nameIsNewList = true;
        for (var i = 0; i < playlist.length; i++) {
            if (playlist[i]['list'] === normalizedName) {
                nameIsNewList = false;
            }
        }
        if (nameIsNewList)  {
            localStorage.setItem("normalizedName", normalizedName);
            localStorage.setItem("displayName", displayName);
            window.location.href = 'playlistcreation.html';
        }
        else {
            $(".notify").toggleClass("active");
            $("#notifyType").toggleClass("success");

            setTimeout(function(){
                $(".notify").removeClass("active");
                $("#notifyType").removeClass("success");
            },2000);
        }
    })
});




