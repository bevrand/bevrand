import {Given} from "cypress-cucumber-preprocessor/steps";

const url = "/";

Given(/^I am a new user using (.*?)$/, (device) => {
    cy.viewport(device);
    cy.visit(url);
    cy.title().should('eq', 'Beverage Randomizer');
});
