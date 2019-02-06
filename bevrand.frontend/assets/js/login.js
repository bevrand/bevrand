
var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    $('#loggedOnButton').hide();
});

$( "#loginForm").submit(function( event ) {
    var password = $('#passwordField').val();
    var email = $('#emailField').val()

    var userToLogon = mapUsertoJson("usertotestwith", email, password);
    loginUser(userToLogon)
    event.preventDefault()
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