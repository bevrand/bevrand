import {Then, When} from "cypress-cucumber-preprocessor/steps";

When(/^I arrive at my profile$/,() => {
    cy.url().should('include', '/profile')
});

When(/^I click on the add playlist button$/,() => {
    cy.get('#addPlayList').click()
});

When(/^I click (.+)$/,(button) => {
    if (button === 'create') {
        cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-footer > div:nth-child(2) > button')
            .click();
    }
    else {
        cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-footer > div:nth-child(1) > button')
            .click()
    }
});

When(/^I get the time to get some drinks alert when pressing (.+)$/,(button) => {
    if (button === 'create') {
        cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-text').then(($validationText) => {
            expect($validationText.text()).to.contain('Time to get some')
        });

        cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-footer > div > button')
            .click();
    }
});

When(/^I choose add the preseeded playlist$/,() => {
    cy.fixture('sampleplaylist.json')
        .then((playlist) => {
            cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-content > input')
                .type(playlist.displayName);
        })
});

When(/^I add a few valid drinks in the playlistcreation screen$/,() => {
    cy.get('#creationArea > div > input').type('beer');
    cy.get('#creationArea > div > a > svg').click();
    cy.get('#creationArea > div > input').type('red wine');
    cy.get('#creationArea > div > a > svg').click();
    cy.get('#creationArea > div > input').type('whiskey');
    cy.get('#creationArea > div > a > svg').click();
});

When(/^I save this playlist$/,() => {
    cy.get('#submitButton').click()
});

When(/^I select the dice to play the playlist$/,() => {
    cy.get('#dicebutton').click()
});

Then(/^I should be rerouted to the (.+) page$/,(page) => {
    cy.url().should('include', '/' + page)
});

Then(/^I should get a validation of success$/,() => {
    cy.get('@playlistname').then(($text =>
        cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-text').then(($validationText) => {
            expect($validationText.text()).to.contain($text);
        })));
    cy.get('body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-footer > div > button')
        .click();
});

Then(/^My new playlist should be visible$/,() => {
    cy.get('@playlistname').then(($text =>
        cy.get('#readablemain > div.loginarea > div')
            .children()
            .its('length')
            .should('be.gt', 1)
    ))}
);

Then(/^I should get an error with the text (.+)$/, (errorText) => {
    cy.get("body > div.swal-overlay.swal-overlay--show-modal > div > div.swal-text").then(($error) => {
        cy.log(errorText)
        expect($error.text()).to.contain(errorText);
    });
});
