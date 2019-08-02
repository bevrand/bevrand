import {Then} from "cypress-cucumber-preprocessor/steps";

Then(/^I should get an error with the term (.+) and (.+)$/, (message, errorText) => {
    cy.get("body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-title").then(($error) => {
        expect($error.text()).to.contain(message);
    });

    cy.get("body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-text").then(($error) => {
        expect($error.text()).to.contain(errorText);
    });
});
