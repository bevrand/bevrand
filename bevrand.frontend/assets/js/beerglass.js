$("#randomizebutton").click(function() {

    $("#randomizebutton").hide();

    $('#randomized_drink').text(''); // Clear text

    $('#liquid') // Lower liquid level
        .animate({
            height: '-10px'
        }, 2000);

    $('.beer-foam') // Lower beer foam
        .animate({
            bottom: '20px'
        }, 1700);

    $('.pour') // Start pouring down
        .delay(0)
        .animate({
            height: '360px'
        }, 2500)
        .slideDown(500);
        //.delay(1600);

    $('#liquid') // I Said Fill 'Er Up!
        //.delay(100)
        .animate({
            height: '200px'
        }, 2150);

    $('.beer-foam') // Keep that Foam Rollin' Toward the Top! Yahooo!
        //.delay(100)
        .animate({
            bottom: '200px'
        }, 2800);

    $('.pour') // Stop pouring beer
        .animate({
            height: '0px'
        }, 1500)
        //.delay(1600)
        .slideUp(500);

    window.setTimeout(function () {
        $('#randomized_drink').text('Beer');
    }, 4500);

    window.setTimeout(function () {
        $('#randomizebutton')
            .text("Randomize from this list again?")
            .show()
    }, 4500);



});