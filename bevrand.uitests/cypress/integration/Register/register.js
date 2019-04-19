import {Then, When} from "cypress-cucumber-preprocessor/steps";

When(/^I register myself using (.+) and (.+) and (.+) and (.+)$/,(username, email, password, repeatPassword) => {
    cy.get('#username')
        .type(username);
    cy.get('#email')
        .type(email);
    cy.get('#password')
        .type(password);
    cy.get('#repeat-password')
        .type(repeatPassword);

    cy.get('#signUpButton').click()
});

Then(`I should be rerouted to the reroute page`,() => {
    cy.url().should('include', '/reroute')
});

Then(`I should not be rerouted to the reroute page`,() => {
    cy.url().should('not.include', '/reroute')
});

Then(`I should end up at my profile with my username filled out`,() => {
    cy.wait(1000);
    cy.url().should('include', '/profile');
    cy.get('@username').then(($text =>
        cy.get('#usernamePersonal').then(($username) => {
            expect($username.text()).to.contain($text);
        }))
    );
});
