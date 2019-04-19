import {When} from "cypress-cucumber-preprocessor/steps";

When(/^I visit the page (.+)$/,(page) => {
    cy.visit(page)
});