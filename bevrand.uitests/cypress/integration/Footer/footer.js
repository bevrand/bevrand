import { Then } from "cypress-cucumber-preprocessor/steps";

Then(/^The footer should be visible and usable$/,() => {
    cy.get('#footer');
    cy.get('#footer > header > h3').then(($footerText) => {
        expect($footerText.text()).to.eq('Wanna reach out?')
    });
    cy.get('#footer > a')
        .should('have.attr', 'href').and('include', 'github.com/bevrand/bevrand');
});
