import {Then, When} from "cypress-cucumber-preprocessor/steps";

let beverageArray = [];

When(`I randomize a drink`,  () => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        expect($randomDrink.text()).to.eq("Press Randomize Button!")
    });
    cy.get('#randomizebutton').click();
    cy.wait(1000);
    cy.get('#randomizedDrink').then(($randomDrink) => {
        expect($randomDrink.text()).to.not.eq("Press Randomize Button!")
    });
});

When(`I select a playlist and view the detail page`,  () => {
    cy.visit('/#playlistCarousel');
    cy.get('#playlistCarousel > div.VueCarousel-wrapper > div').children().then(($playlists) => {
        let randomNumber = getRandomNumber(1, $playlists.length - 1);
        cy.get(`#playlistCarousel > div.VueCarousel-wrapper > div > div:nth-child(${randomNumber})`).within(() => {
            cy.get('#linkToAllDrinks').click();
        });
        cy.get('#detailedBeverages > li')
            .each(($el) => {
                beverageArray.push($el.text())
            });
        cy.get('#dicebutton').click();

        cy.get(`#playlistCarousel > div.VueCarousel-wrapper > div > div:nth-child(${randomNumber}) > span > a.image.featured > img`)
            .click();
    });
    cy.wait(1000);
});

Then(`I should get a result`,() => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        expect($randomDrink.text()).not.to.eq("Press Randomize Button!")
    });
});


Then(`the result should be in the beveragelist from the detail page`,() => {
    let included = false;
    cy.get('#randomizedDrink')
        .then(($randomDrink) => {
            for (let i = 0; i < beverageArray.length; i++) {
                if (beverageArray[i].trim() === $randomDrink.text().trim()) {
                    included = true;
                }
            }
            expect(included).to.be.true;
        });
});

function getRandomNumber(low, high) {
    return Math.floor(Math.random() * (high - low + 1)) + low;
}