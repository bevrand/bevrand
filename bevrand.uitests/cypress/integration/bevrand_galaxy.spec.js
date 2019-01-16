context('Beverage Randomizer Test', () => {
    beforeEach(() => {
        cy.viewport(360, 640);
        cy.visit('http://0.0.0.0')
    });

        describe('Page comes up', function () {
            it('Visits the beverage randomizer', function () {
                cy.title().should('eq', 'The Beverage Randomizer');
            })
        });

    describe('Should be able to use the bevrand flow', function () {
        it('Should be able to enter the selection area', function () {
            cy.get('#letsGetStartedButton').click();
            cy.get('#banner > header > h2').contains('Hi. You\'re looking at ');
        });
        it('Should be able to enter the randomize area', function () {
            cy.get('#letsGetStartedButton').click();
            cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > header > h3 > a').then(($currentList) => {
                let selectedPlayList = $currentList.text().split(' ')[0];
                cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > a > img').click();
                cy.get('#currentlySelectedPlayList').contains(selectedPlayList);
            });
        });
    });

    describe('Randomize functionality works', function () {
        it('Should be able to randomize my drinks', function () {
            cy.get('#letsGetStartedButton').click();
            cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > header > h3 > a').click();
            cy.get('#randomizebutton').click();
            cy.wait(1000);
            cy.get('#randomizebutton').should('not.be.visible');
            // cy.screenshot();
            cy.wait(3500);
            cy.get('#randomizebutton').should('be.visible');
        });
        it('The randomized drink is in the list', function () {
            cy.get('#letsGetStartedButton').click();
            cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > header > h3 > a').click();
            cy.wait(500);
            cy.get('#randomizebutton').click();
            cy.wait(5000);
            cy.get('#randomizedDrink').then(($randomizedOutput) => {
                console.log($randomizedOutput.text());
                let firstDrink = $randomizedOutput.text();
                cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > ul').contains(firstDrink)
            })
        });
        it('Should be able to switch list', function () {
            cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > header > h3 > a').click();
            cy.wait(500);
            cy.get('#currentlySelectedPlayList').then(($currentList) => {
                let selectedPlayList = $currentList.text();
                cy.visit('http://0.0.0.0/#banner');
                cy.get('#page-wrapper > section.carousel > div > article:nth-child(4) > header > h3 > a').click();
                cy.wait(500);
                cy.get('#currentlySelectedPlayList').then(($secondList) => {
                    expect($secondList.text()).not.to.eq(selectedPlayList)
                })
            })
        });
        it('The randomize button text changes after switching list', function () {
            cy.get('#letsGetStartedButton').click();
            cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > header > h3 > a').click();
            cy.get('#randomizebutton').click();
            cy.wait(5000);
            cy.get('#randomizebutton').contains('again');
            cy.visit('http://0.0.0.0/#banner');
            cy.get('#page-wrapper > section.carousel > div > article:nth-child(4) > header > h3 > a').click();
            cy.get('#randomizebutton').then(($buttonText) => {
                expect($buttonText.text()).not.to.eq('Randomize from this list again?');
                expect($buttonText.text()).to.eq('Randomize!')
            })
        });
        it('Should be able to randomize my drinks twice', function () {
            cy.get('#letsGetStartedButton').click();
            cy.get('#page-wrapper > section.carousel > div > article:nth-child(1) > header > h3 > a').click();
            cy.get('#randomizebutton').click();
            cy.wait(1000);
            cy.get('#randomizebutton').should('not.be.visible');
            cy.wait(3500);
            cy.get('#randomizebutton').should('be.visible');
            cy.get('#randomizebutton').then(($buttonText) => {
                expect($buttonText.text()).to.eq('Randomize from this list again?');
            });
            cy.get('#randomizedDrink').then(($randomizedOutput) => {
                expect($randomizedOutput.text()).not.to.eq(' ');
            });
            cy.get('#randomizebutton').click();
            cy.wait(1000);
            cy.get('#randomizebutton').should('not.be.visible');
            // cy.screenshot();
            cy.wait(3500);
            cy.get('#randomizebutton').should('be.visible');
            cy.get('#randomizebutton').then(($buttonText) => {
                expect($buttonText.text()).to.eq('Randomize from this list again?');
            });
            cy.get('#randomizedDrink').then(($randomizedOutput) => {
                expect($randomizedOutput.text()).not.to.eq(' ');
            });
        });
    });
    describe('Footer has hyperlinks', function () {
        it('Should be able to reach footer', function () {
            cy.visit('http://0.0.0.0/#footer');
            cy.get('#footer > div > div > div > section > header > h3').then(($footerText) => {
                expect($footerText.text()).to.eq('Wanne reach out?');
            })});
        it('Should be able to use footer button github', function () {
            cy.visit('http://0.0.0.0/#footer');
            cy.get('#footer > div > div > div > section > ul > li > a')
                .should('have.attr', 'href').and('include', 'github.com/bevrand');
        })
    });
});

/*


function makeRandomString(numberOfChars) {
    let text = ""
    let possible = "abcdefghijklmnopqrstuvwxyz0123456789"

    for (let i = 0; i < numberOfChars; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;

}
})

*/