import {Then, When} from "cypress-cucumber-preprocessor/steps";

When(`I select any playlist`,  () => {
    cy.visit('/#playlistCarousel');
    cy.wait(500);
    cy.get('#playlistCarousel > div.VueCarousel-wrapper > div').children().then(($playlists) => {
        let randomNumber = getRandomNumber(1, $playlists.length - 1);
        cy.get(`#playlistCarousel > div.VueCarousel-wrapper > div > div:nth-child(${randomNumber})`).within(() => {
            cy.get('#beverageList').as('selectedBeverageList');
            cy.get('> span > a.image.featured > img').click();
        });
    });
    cy.wait(750);
});

When(`I randomize a drink`,  () => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        expect($randomDrink.text()).to.eq("Press Randomize Button!")
    });
    cy.get('#randomizebutton').click();
    cy.wait(1000);
});

When(`I randomize a drink a second time`,  () => {
    cy.get('#randomizebutton').click();
    cy.wait(1000);
});

Then(`I should get a result`,() => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        expect($randomDrink.text()).not.to.eq("Press Randomize Button!")
    });
});

Then(`the result should be in the selected playlist`,() => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        cy.get('@selectedBeverageList').contains($randomDrink.text())
    });
});

function getRandomNumber(low, high) {
    return Math.floor(Math.random() * (high - low + 1)) + low;
}