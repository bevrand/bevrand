import {Then, When} from "cypress-cucumber-preprocessor/steps";

When(/^I log myself in using (.+) and (.+)$/,(email, password ) => {
    cy.get('#email')
        .type(email);
    cy.get('#password')
        .type(password);

    cy.get('#loginButton').click()
});

Then(`I should be rerouted to the profile page`,() => {
    cy.get('#loginForm > section > div');
    cy.wait(1000);
    cy.url().should('include', '/profile')
});

Then(`I should end up at my profile with my username filled out`,() => {
    cy.fixture('standarduser.json')
        .then((credentials) => {
            cy.get('#usernamePersonal').then(($username) => {
                expect($username.text()).to.contain(credentials.username);
            });
        })
});