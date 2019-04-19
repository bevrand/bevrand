import {Given} from "cypress-cucumber-preprocessor/steps";

const url = "/";

Given(/^I am a new user using (.*?)$/, (device) => {
    cy.visit(url);
    cy.viewport(device);
    cy.title().should('eq', 'Beverage Randomizer');
    cy.get('#linkToAllDrinks');
});
