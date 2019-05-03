import { When } from "cypress-cucumber-preprocessor/steps";

When(/^I choose a random name as my playlist name$/,(text) => {
    let randomPlaylist = "CAPS" + createRandomString(15);
    cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-content > input')
        .type(randomPlaylist);
    cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-content > input')
        .invoke('val')
        .as('playlistname');
});

When(`I register myself as a new user`,  () => {
    let username = createRandomString(15);
    let email = createRandomString(10) + "@" + createRandomString(5) + ".net";
    let password = createRandomString(15);

    cy.get('#username').type(username);
    cy.get('#email').type(email);
    cy.get('#password').type(password);
    cy.get('#repeat-password').type(password);

    cy.get('#username')
        .invoke('val')
        .as('username');

    cy.get('#signUpButton').click()
});

When(`I select any playlist`,  () => {
    cy.visit('/#playlistCarousel');
    cy.get('#playlistCarousel > div.VueCarousel-wrapper > div').children().then(($playlists) => {
        let randomNumber = getRandomNumber(1, $playlists.length - 1);
        cy.get(`#playlistCarousel > div.VueCarousel-wrapper > div > div:nth-child(${randomNumber})`).within(() => {
            cy.get('#beverageList').as('selectedBeverageList');
            cy.get('> span > a.image.featured > img').click();
        });
    });
    cy.wait(1000);
});

When(`I select another playlist by image`,  () => {
    //cy.visit('/#playlistCarousel');
    cy.get('#playlistCarousel > div.VueCarousel-wrapper > div').children().then(($playlists) => {
        let randomNumber = getRandomNumber(2, $playlists.length - 2);
        cy.get(`#playlistCarousel > div.VueCarousel-wrapper > div > div:nth-child(${randomNumber})`).within(() => {
            cy.get('#playlistName > h3')
                .as('secondPlaylist');
            cy.get('> span > a.image.featured > img').click();
        });
    });
   // cy.wait(1000);
});

function getRandomNumber(low, high) {
    return Math.floor(Math.random() * (high - low + 1)) + low;
}

function createRandomString(numberOfChars) {
    let text = "";
    let possible = "abcdefghijklmnopqrstuvwxyz0123456789";

    for (let i = 0; i < numberOfChars; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}