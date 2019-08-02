import {When, Then} from "cypress-cucumber-preprocessor/steps";

When(`I select the first playlist by image`,  () => {
    cy.get('#letsGetStartedButton').click();
    cy.url().should('include', '#playlistCarousel');
    cy.get('#playlistCarousel > div.VueCarousel-wrapper > div > div:nth-child(1)').within(() => {
        cy.get('#playlistName > h3')
            .as('selectedPlayList');
        cy.get('> span > a.image.featured > img').click();
    });
    cy.wait(750)
});

When(`I select the last playlist`,  () => {
    cy.get('#LoginAndRegister').click()
});

When(`I swipe to the next page`,  () => {
    cy.get('#letsGetStartedButton').click();
    cy.url().should('include', '#playlistCarousel');

    cy.get('#playlistCarousel > div.VueCarousel-wrapper > div')
        .trigger('mousedown', { which: 1 })
        .trigger('mousemove', { clientX: 120, clientY: 300 })
        .trigger('mouseup', {force: true})
});

Then(`The headertext matches the selected playlist`,() => {
    cy.url().should('include', '#main');
    cy.get('@selectedPlayList').invoke('text').then((chosenPlaylist) => {
        cy.get('#currentlySelectedPlayList').invoke('text').should((selectedPlaylist) => {
            expect(chosenPlaylist.trim()).to.eq(selectedPlaylist.trim())
        })
    });
});

Then(`The headertext matches the secondly selected playlist`,() => {
    cy.url().should('include', '#main');
    cy.get('@secondPlaylist').invoke('text').then((chosenPlaylist) => {
        cy.get('#currentlySelectedPlayList').invoke('text').should((selectedPlaylist) => {
            expect(chosenPlaylist.trim()).to.eq(selectedPlaylist.trim())
        })
    });
});

Then(`The headertext does not match the first selected playlist`,() => {
    cy.url().should('include', '#main');
    cy.get('@selectedPlayList').invoke('text').then((chosenPlaylist) => {
        cy.get('#currentlySelectedPlayList').invoke('text').should((selectedPlaylist) => {
            expect(chosenPlaylist.trim()).not.to.eq(selectedPlaylist.trim())
        })
    });
});

Then(`The active first slide should not be the active slide` ,() => {
    cy.get('#playlistCarousel > div.VueCarousel-pagination > div > button:nth-child(1)')
        .should('not.have.class', 'VueCarousel-dot--active');
    cy.get('#playlistCarousel > div.VueCarousel-pagination > div > button:nth-child(1)')
        .should('have.class', 'VueCarousel-dot');
    cy.get('#playlistCarousel > div.VueCarousel-pagination > div > button:nth-child(2)')
        .should('have.class', 'VueCarousel-dot--active')
});

Then(`I should be rerouted to the login page` ,() => {
    cy.url().should('include', '/login');
});
