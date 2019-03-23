function redirectToHomepage(count) {
    var countdown = setInterval(function(){
        document.getElementById("redirectionText").textContent = "Redirecting you to your profile in " + count + " seconds";
        if (count === 0) {
            clearInterval(countdown);
            location.href = "profile.html";
        }
        count--;
    }, 1000);
}