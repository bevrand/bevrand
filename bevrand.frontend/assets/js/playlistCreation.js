var beverages = [];
var normalizedPlayListName = '';
var displayName = '';
var username = '';
var imageUrl = 'https://static.beveragerandomizer.com/file/beveragerandomizer/images/users/standardimage.png';

var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    $('#beverageAdditionField').hide();
    $('#addBeverage').hide();
    $('#cancelAddBeverage').hide();
    $('#getRecommandations').hide();
    $('#successButton').hide();
    displayName = localStorage.getItem("displayName");
    normalizedPlayListName = localStorage.getItem("normalizedName");
    var storedBeverages = localStorage.getItem("beverages");
    if (storedBeverages) {
        beverages = storedBeverages;
    }
    token = localStorage.getItem("jwt");
    username = parseJwt(token)['username'];

    $('#playlistCreationName')
        .text("Playlist name: " + displayName);
});

function addNewBeverage() {
    $('#beverageAdditionField').show();
    $('#addBeverage').show();
    $('#cancelAddBeverage').show();
}

$("#cancelAddBeverage").click(function () {
    $('#beverageAdditionField').hide();
    $('#addBeverage').hide();
    $('#cancelAddBeverage').hide();
});

$("#addBeverage").click(function () {
    var beverageName = document.getElementById("beverageAdditionField").value;
    if (beverageName === "" ||  beverages.includes(beverageName)){
        document.getElementById("notifyType").textContent = "This drink is already included";
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function () {
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        }, 1000);
        return
    }

    if (beverageName.length <= 1) {
        document.getElementById("notifyType").textContent = "Your beverage seems to be too short";
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function () {
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        }, 2000);
        return
    }

    beverages.push(beverageName);
    appendBeverages(beverageName)
    document.getElementById("beverageAdditionField").value = ""
});

function deleteDrink(link) {
    var text = link.parentNode.textContent;
    for (var i = 0; i < beverages.length; i++) {
        if (text.trim() === beverages[i].trim()){
            beverages.splice(i, 1);
        }
    }
    link.parentNode.parentNode.removeChild(link.parentNode);
}

function editDrink(link) {
    var text = link.parentNode.textContent.trim();
    document.getElementById("beverageAdditionField").value = text;
    deleteDrink(link)
}


function appendBeverages(beverage) {
    var beverageHtml = addDrinksToPlaylist(beverage);
    $('#playListCreationDrinks').append(beverageHtml);
}

function addDrinksToPlaylist(beverage) {
    return "<li>" + beverage + " <i onclick=\"editDrink(this)\" style=\"margin-left: 0.5em\" class=\"fa fa-pencil\"></i> <i onclick=\"deleteDrink(this)\" style=\"margin-left: 0.5em\" class=\"fa fa-trash\"></i></li>"

}

$("#createPlayList").click(function () {
    var randomizeList = mapDrinksToJson();
    if (beverages.length <= 1) {
        document.getElementById("notifyType").textContent = "You need at least two drinks in your list";
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        },2000);
        return
    }
    postDrinkToBackEnd(randomizeList);

});

$("#successButton").click(function ()  {
    window.location.href = 'index.html';
});

function postDrinkToBackEnd(randomizeList) {
    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/api/user`,
        data: randomizeList,
        contentType: "application/json",
        success: function () {
            $('#beverageAdditionField').hide();
            $('#addBeverage').hide();
            $('#cancelAddBeverage').hide();
            $('#createPlayList').hide();
            $('#successButton').show();
        },
        error: function (error) {
            if (error.status === 400) {
                document.getElementById("notifyType").textContent = error.responseJSON['Error']
                if (error.responseJSON['Meta'] != null) {
                    document.getElementById("notifyType").textContent = error.responseJSON['Meta']['beverages'][0]
                }
                $(".notify").toggleClass("active");
                $("#notifyType").toggleClass("success");

                setTimeout(function(){
                    $(".notify").removeClass("active");
                    $("#notifyType").removeClass("success");
                },2000);
            }
            if (error.status === 500 || error.status === 503) {
                document.getElementById("notifyType").textContent = "Servers appear to be down"
                $(".notify").toggleClass("active");
                $("#notifyType").toggleClass("success");

                setTimeout(function(){
                    $(".notify").removeClass("active");
                    $("#notifyType").removeClass("success");
                },2000);

            }
        }
    });
}

function mapDrinksToJson() {
    var playlist = JSON.stringify({
        beverages: beverages,
        displayName: displayName,
        imageUrl: imageUrl,
        list: normalizedPlayListName,
        user: username
    });

    return playlist
}