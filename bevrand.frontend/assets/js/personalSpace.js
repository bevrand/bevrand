var username = '';
var token = '';

var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost'
};

$(document).ready(function () {
    token = localStorage.getItem("jwt");
    console.log(token);
    var jwtDecoded = parseJwt(token);
    username = jwtDecoded['username'];
    var emailAddress = "place@holder.nl"

    $('#personalSpaceUsername')
        .text(username + "'s personal workspace");
    $('#usernamePersonal')
        .text(`Username: ${username}`);
    $('#emailAddressPersonal')
        .text(`Email: ${emailAddress}`);

    $('#playListCreationField').hide();
    $('#okPlayListCreation').hide();
    $('#cancelPlayListCreation').hide();

    $('#usernamePersonal')
        .text("Username: " + username);

    getPersonalPlaylists(username, function (playlists) {
        console.log(playlists)
        appendPlaylistToWorkspace(playlists['result']);
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
        headers: {"x-api-token": token },
        url: `${config.proxyHostname}/playlist-api/v1/private/${username}`,
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
    getPersonalPlaylists(username, function (playlist) {
        var nameIsNewList = true;
        for (var i = 0; i < playlist['result'].length; i++) {
            if (playlist['result'][i]['list'] === normalizedName) {
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




