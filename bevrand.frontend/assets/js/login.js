
var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};


var username = "";
var loggedOn = "";

$(document).ready(function () {
    $('#loggedOnButton').hide();
    $('#logoutButton').hide();
    loggedOn = localStorage.getItem("loggedOn");
    if (loggedOn === "loggedOn"){
        $('#loginButton').hide();
        $('#loggedOnButton').show();
        $('#logoutButton').show();
        username = localStorage.getItem("username");
        $('#loginForm').textContent = `Welcome ${username}`
    }
});

$("#loginForm").submit(function( event ) {
    var password = $('#passwordField').val();
    var email = $('#emailField').val()
    var username = "joeri";

    var userToLogon = mapUsertoJson(username, email, password);
    loginUser(userToLogon);
    localStorage.setItem("username", username);
    localStorage.setItem("loggedOn", "loggedOn");
    event.preventDefault();
});

$("#logoutButton").click(function () {
    $('#logoutButton').hide();
    $('#loginButton').show();
    $('#loggedOnButton').hide();
    localStorage.setItem("loggedOn", "");
});

function loginUser(userList) {
    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/api/login`,
        data: userList,
        contentType: "application/json",
        success: function (data) {
            console.log(data)
            $('#loginButton').hide();
            $('#loggedOnButton').show();
            $('#logoutButton').show();
            return
        },
        error: function (error) {
            console.log(error)
            if (error.status === 401) {
                document.getElementById("notifyType").textContent = "Email or password incorrect";
                $(".notify").toggleClass("active");
                $("#notifyType").toggleClass("success");

                setTimeout(function(){
                    $(".notify").removeClass("active");
                    $("#notifyType").removeClass("success");
                },4000);
            }
            if (error.status === 500 || error.status === 503) {
                document.getElementById("notifyType").textContent = "Servers appear to be down"
                $(".notify").toggleClass("active");
                $("#notifyType").toggleClass("success");

                setTimeout(function(){
                    $(".notify").removeClass("active");
                    $("#notifyType").removeClass("success");
                },4000);
            }

        }
    });
}

function mapUsertoJson(username, email, password) {
    var userList = JSON.stringify({
        "userName": username,
        "emailAddress": email,
        "passWord": password,
    });

    return userList
}