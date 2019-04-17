import {Then, When} from "cypress-cucumber-preprocessor/steps";

let username = '';

When(`I register myself as a new user`,  () => {
    username = createRandomString(15);
    let email = createRandomString(10) + "@" + createRandomString(5) + ".net";
    let password = createRandomString(15);

    cy.get('#username').type(username);
    cy.get('#email').type(email);
    cy.get('#password').type(password);
    cy.get('#repeat-password').type(password);

    cy.get('#signUpButton').click()
});

Then(`I should be rerouted to the reroute page`,() => {
    cy.url().should('include', '/reroute');
    cy.url().should('include', username);
});

Then(`I should end up at my profile with my username filled out`,() => {
    cy.wait(2000);
    cy.url().should('include', '/profile');
    cy.get('#usernamePersonal').then(($username) => {
        expect($username.text()).to.contain(username);
    });

});

function createRandomString(numberOfChars) {
    let text = "";
    let possible = "abcdefghijklmnopqrstuvwxyz0123456789";

    for (let i = 0; i < numberOfChars; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;

}