import {Given } from "cypress-cucumber-preprocessor/steps";

const url = "/";

Given(/^I am a registering user using (.*?)$/, (device) => {
    cy.viewport(device);
    cy.visit(url + "register");
    cy.title().should('eq', 'Beverage Randomizer');
});
