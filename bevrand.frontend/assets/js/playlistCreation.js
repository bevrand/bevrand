var beverages = [];
var normalizedPlayListName = '';
var displayName = '';
var user = '';
var imageUrl = 'https://static.beveragerandomizer.com/file/beveragerandomizer/images/users/standardimage.png';



var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    displayName = localStorage.getItem("displayName");
    normalizedPlayListName = localStorage.getItem("normalizedName");
    user = localStorage.getItem("username");
    console.log(displayName)
    console.log(normalizedPlayListName)

    $('#playlistCreationName')
        .text(displayName);
});


function createPlayList() {
    var playlist = `{
        "beverages": ${beverages},
        "displayName": ${displayName},
        "imageUrl": ${imageUrl},
        "list": ${normalizedPlayListName},
        "user": ${user}
    }`
    return playlist
}