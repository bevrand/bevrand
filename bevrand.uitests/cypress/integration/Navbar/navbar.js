import { Then } from "cypress-cucumber-preprocessor/steps";

const homepageText = 'Bevrand';

When(/^I open the navbar menu$/,() => {
    cy.get('#page-wrap > div > div > div.bm-burger-button').click();
    cy.wait(500);
});

When(/^I press logout on the navbar$/,() => {
    cy.url().should('include', '/profile');

    cy.get('#page-wrap > div > div > div.bm-burger-button').click();
    cy.wait(500);
    cy.get('#navlinkLogout').click();
});

Then(/^The navbar should be visible and usable$/,() => {
    cy.get('#page-wrap > div > div > div.bm-menu');

    headerLinkContainsText(homepageText);
});

Then(/^The logged off status should be shown$/,() => {
    cy.get('#page-wrap > div > div > div.bm-menu');

    headerLinkContainsText(homepageText);

    cy.get('#headerLink')
        .should('have.attr', 'href').and('include', '/');
    cy.get('#navlinkLogin')
        .should('have.attr', 'href').and('include', '/login');
    cy.get('#navlinkRegister')
        .should('have.attr', 'href').and('include', '/register');
});

Then(/^The logged on status should be shown$/,() => {
    cy.url().should('include', '/profile');

    cy.get('#page-wrap > div > div > div.bm-burger-button').click();
    cy.wait(500);

    cy.get('#page-wrap > div > div > div.bm-menu');
    headerLinkContainsText(homepageText);

    cy.get('#headerLink')
        .should('have.attr', 'href').and('include', '/');
    cy.get('#navlinkProfile')
        .should('have.attr', 'href').and('include', '/profile');
    cy.get('#navlinkLogout').then(($navbarText) => {
        expect($navbarText.text()).to.contain('Logout')
    });
});

Then(`I should be rerouted to the login page`,() => {
    cy.url().should('include', '/login')
});

function headerLinkContainsText(assertText) {
    cy.get('#headerLink').then(($navbarText) => {
        expect($navbarText.text()).to.contain(assertText)
    });
}