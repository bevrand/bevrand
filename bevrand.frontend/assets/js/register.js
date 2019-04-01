var id = '';

var config = {
    proxyHostname: 'https:' == document.location.protocol ? '' : 'http://localhost:4540'
};

$(document).ready(function () {
    $("#redirectionText").hide();
});

$( "#registrationForm").submit(function( event ) {
    var password = $('#passwordField').val();
    var passwordCheck = $('#passwordVerificationField').val();

    var passwordValid = validatePassword(password, passwordCheck, 3, 20);

    var username = $('#usernameField').val();
    var usernameValid = validateUsername(username, 3, 20);

    var email = $('#emailField').val();
    var emailValid = validateEmail(email, 5, 40);
    if (!passwordValid || !usernameValid || !emailValid) {
        event.preventDefault();
        return
    }
    var userList = mapUsertoJson(username, email, password);
    registerUser(userList);
    event.preventDefault();
});


function validateUsername(username, min, max) {
    var usernameLength = username.length;
    if (usernameLength > max || usernameLength < min)
    {
        document.getElementById("notifyType").textContent =
            "Username length should be between "+ min +" to "+max
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        },2000);

        return false;
    }
    return true;
}

function validateEmail(email, min, max) {
    var emailLength = email.length;
    if (emailLength > max || emailLength < min)
    {
        document.getElementById("notifyType").textContent =
            "Email length should be between "+ min +" to "+max;
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        },2000);
        return false;
    }
    return true;
}

function validatePassword(password, checkPassword, min, max)
{
    var validated = validatePasswordsAreEqual(password, checkPassword);
    if (!validated){
        document.getElementById("notifyType").textContent =
            "Password are not equal";
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        },2000);

        return false;
    }
    var passwordLength = password.length;
    if (passwordLength > max || passwordLength < min)
    {
        document.getElementById("notifyType").textContent =
            "Password length should be between "+ min +" to "+max;
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        },2000);
        return false;
    }
    return true;
}

function validatePasswordsAreEqual(password, checkPassword){
    return password === checkPassword;
}

function registerUser(userList) {
    $.ajax({
        type: "POST",
        url: `${config.proxyHostname}/api/register`,
        data: userList,
        contentType: "application/json",
        success: function (data) {
            id = data['id'];
            $("#registerButton").hide();
            $("#usernameField").hide();
            $("#emailField").hide();
            $("#passwordField").hide();
            $("#passwordVerificationField").hide();
            loginUser(userList);
        },
        error: function (error) {
            if (error.status === 400) {
                var stringError = error.responseJSON['message'];
                var splitError = JSON.parse(stringError.substring(stringError.indexOf('-') +1));

                var alreadyExists = splitError['Error'].includes("already exists");

                if(alreadyExists){
                    var text = " already exists please pick another";
                    var type  = splitError['Error'].split(":")[0];
                    document.getElementById("notifyType").textContent = type + text;
                }
                else {
                    document.getElementById("notifyType").textContent = splitError['Error'];
                }

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