import {Given, When} from "cypress-cucumber-preprocessor/steps";

const url = "/";

Given(/^I am a registered user logging in using (.*?)$/, (device) => {
    cy.viewport(device);
    cy.visit(url + "login");
    cy.title().should('eq', 'Beverage Randomizer');
});

When(/^I enter my credentials and login$/,() => {
    cy.fixture('standarduser.json')
        .then((credentials) => {
            cy.get('#username')
                .type(credentials.username);
            cy.get('#email')
                .type(credentials.emailAddress);
            cy.get('#password')
                .type(credentials.password);
        });
    cy.get('#loginButton').click()
});