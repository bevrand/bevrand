
var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

var token = "";
var username = "";

$(document).ready(function () {
    $("#redirectionText").hide();
    token = localStorage.getItem("jwt");

    if (token){
        username = parseJwt(token)['username'];
        toggleLoginFields();
        $("#redirectionText").show();
        redirectToHomepage(3);
    }
});

$("#loginForm").submit(function( event ) {
    var password = $('#passwordField').val();
    var email = $('#emailField').val();
    username = $('#usernameField').val();

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
            toggleLoginFields()
        },
        error: function (error) {
            console.log(error);
            if (error.status === 401) {
                document.getElementById("notifyType").textContent = "Email or password incorrect";
                $(".notify").toggleClass("active");
                $("#notifyType").toggleClass("success");

                setTimeout(function(){
                    $(".notify").removeClass("active");
                    $("#notifyType").removeClass("success");
                },4000);
            }
            if (error.status === 404) {
                document.getElementById("notifyType").textContent = "Username or email could not be found";
                $(".notify").toggleClass("active");
                $("#notifyType").toggleClass("success");

                setTimeout(function(){
                    $(".notify").removeClass("active");
                    $("#notifyType").removeClass("success");
                },4000);
            }
            if (error.status === 500 || error.status === 503) {
                document.getElementById("notifyType").textContent = "Servers appear to be down";
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

function toggleLoginFields() {
    document.getElementById("welcomeBannerText").textContent = `Welcome ${username}`;
    $('#loginButton').hide();

    $('#usernameField').hide();
    $('#emailField').hide();
    $('#passwordField').hide();

    $('#accountText').hide();
    $('#registerLink').hide();

    $("#redirectionText").show();
    redirectToHomepage(3);
}

function mapUsertoJson(username, email, password) {
    return JSON.stringify({
        "userName": username,
        "emailAddress": email,
        "passWord": password,
    });
}
