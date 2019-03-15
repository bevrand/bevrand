
var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

var token = "";

$(document).ready(function () {
    $('#loggedOnButton').hide();
    $('#profileButton').hide();
    token = localStorage.getItem("jwt");

    if (token){
        console.log(token)
        $('#loginButton').hide();
        $('#loggedOnButton').show();
        $('#profileButton').show();
        var username = parseJwt(token)['username'];
        $('#loginForm').textContent = `Welcome ${username}`
    }
});

$("#loginForm").submit(function( event ) {
    var password = $('#passwordField').val();
    var email = $('#emailField').val();
    var username = $('#usernameField').val();

    var userToLogon = mapUsertoJson(username, email, password);
    loginUser(userToLogon);
    event.preventDefault();
});

function loginUser(userList) {
    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/api/login`,
        data: userList,
        contentType: "application/json",
        success: function (data) {
            localStorage.setItem("jwt", data['token']);
            $('#loggedOnButton').show();
            $('#profileButton').show();
            $('#loginButton').hide();
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

function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(window.atob(base64));
}