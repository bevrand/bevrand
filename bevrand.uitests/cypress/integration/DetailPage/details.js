import {Then, When} from "cypress-cucumber-preprocessor/steps";

When(/^I click on more details for the playlist with position (.+)$/,(number) => {
    cy.get(`#playlistCarousel .VueCarousel-wrapper > div div:nth-child(${number})`).within(() => {
        cy.get('#playlistName > h3')
            .as('selectedPlayList');
        cy.get('#linkToAllDrinks')
            .click()
    });
});

When(/^I click the dice icon to select the playlist$/,() => {
    cy.get('#dicebutton').click()
});

Then(`I should be rerouted to the details page`,() => {
    cy.url().should('include', '/playlistdetails')
});

Then(/^I should see a list with (.+) drinks$/,(numberOfDrinks) => {
    cy.get('#detailedBeverages > li').should('have.length', numberOfDrinks)
});

