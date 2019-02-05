

$( "#registrationForm").submit(function( event ) {
    var password = $('#passwordField').val()
    var passwordCheck = $('#passwordVerificationField').val()

    var passwordValid = validatePassword(password, passwordCheck, 5, 20)

    var username = $('#usernameField').val()
    var usernameValid = validateUsername(username, 3, 20)

    var email = $('#emailField').val()
    var emailValid = validateEmail(email, 5, 40)
    if (!passwordValid || !usernameValid || !emailValid) {
        event.preventDefault()
    }
    var user = mapUsertoJson()
    registerUser(user)
    event.preventDefault()
});


function validateUsername(username, min, max) {
    var usernameLength = username.length;
    if (usernameLength >= max || usernameLength < min)
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
    if (emailLength >= max || emailLength < min)
    {
        document.getElementById("notifyType").textContent =
            "Email length should be between "+ min +" to "+max
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
    var validated = validatePasswordsAreEqual(password, checkPassword)
    if (!validated){
        document.getElementById("notifyType").textContent =
            "Password are not equal"
        $(".notify").toggleClass("active");
        $("#notifyType").toggleClass("success");

        setTimeout(function(){
            $(".notify").removeClass("active");
            $("#notifyType").removeClass("success");
        },2000);

        return false;
    }
    var passwordLength = password.length;
    if (passwordLength >= max || passwordLength < min)
    {
        document.getElementById("notifyType").textContent =
            "Password length should be between "+ min +" to "+max
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
        success: function () {
            alert("jeej")
        },
        error: function (error) {
            if (error.status === 400) {
                console.log(error.responseJSON)
                document.getElementById("notifyType").textContent = error.responseJSON['Error']
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

function mapUsertoJson(username, email, password) {
    var userList = JSON.stringify({
        "userName": username,
        "emailAddress": email,
        "passWord": password,
        "active": true
    });

    return userList
}