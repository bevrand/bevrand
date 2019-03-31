$("#randomizebutton").click(function() {

    $("#randomizebutton").hide();
    $('#randomizedDrink').hide();

    $('.pour').css({
        height: '0px',
        marginTop: '0px'});

    $('.pour') // Start pouring down
        .animate({
            height: '360px'
        }, 2500)
        .slideDown(500);

    $('#liquid') // Lower liquid level
        .animate({
            height: '-10px'
        }, 1200);

    $('.beer-foam') // Lower beer foam
        .animate({
            bottom: '20px'
        }, 1000);

    $('#liquid') // I Said Fill 'Er Up!
        .delay(1000)
        .animate({
            height: '200px'
        }, 2000);

    $('.beer-foam') // Keep that Foam Rollin' Toward the Top! Yahooo!
        .delay(1000)
        .animate({
            bottom: '200px'
        }, 2400);

    $('.pour') // Stop pouring beer
        .animate({
            height: '0px',
            marginTop: '360px'
        }, 1500)
        //.delay(1600)
        .slideUp(500);

    window.setTimeout(function () {
        $('#randomizebutton')
            .text("Randomize from this list again?")
            .show()
        $('#randomizedDrink')
            .show()
        $('#navbar')
            .show()
    }, 4500);

});