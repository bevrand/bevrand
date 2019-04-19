import {Then, When} from "cypress-cucumber-preprocessor/steps";

When(`I randomize a drink`,  () => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        expect($randomDrink.text()).to.eq("Press Randomize Button!")
    });
    cy.get('#randomizebutton').click();
    cy.wait(1000);
});

When(`I randomize a drink a second time`,  () => {
    cy.get('#randomizebutton').click();
    cy.wait(1000);
});

Then(`I should get a result`,() => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        expect($randomDrink.text()).not.to.eq("Press Randomize Button!")
    });
});

Then(`the result should be in the selected playlist`,() => {
    cy.get('#randomizedDrink').then(($randomDrink) => {
        cy.get('@selectedBeverageList').contains($randomDrink.text())
    });
});