import {Then} from "cypress-cucumber-preprocessor/steps";

Then(/^I should be rerouted to the homepage with anchor (.+)$/,(anchor) => {
    cy.url().should('include', anchor)
});

Then(/^the selected playlist should be (.+)$/,(name) => {
    cy.get('#currentlySelectedPlayList').invoke('text').should((selectedPlaylist) => {
        expect(name.trim()).to.eq(selectedPlaylist.trim())
    })
});
