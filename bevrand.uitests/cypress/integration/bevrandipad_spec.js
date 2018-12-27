let userName = '';
let passWord = '';

context('Beverage Randomizer Test', () => {
    beforeEach(() => {
        cy.viewport('ipad-2');
        cy.visit('http://0.0.0.0')
    }),

        describe('Page comes up', function () {
            it('Visits the beverage randomizer', function () {
                cy.title().should('eq', 'The Beverage Randomizer')
            })
        })

    describe('Randomize functionality works', function () {
        it('Should be able to randomize my drinks', function () {
            cy.get('#letsGetStartedButton').click()
            cy.get('#randomizeButton').click()
            cy.get('#randomizedOutput').contains('randomized')
        })
        it('Should be able to switch list', function () {
            cy.get('#letsGetStartedButton').click()
            cy.get("#currentlySelectedPlaylist").then(($currentList) => {
                const firstList = $currentList.text()
                cy.get('#chooseListBottomButton').click()
                cy.get('#playlists > div > div > div:nth-child(2) > a > div').click()
                cy.get("#currentlySelectedPlaylist").then(($secondList) => {
                    expect($secondList.text()).not.to.eq(firstList)
                })
            })
        })
        it('The randomized drink is in the list', function () {
            cy.get('#letsGetStartedButton').click()
            cy.get('#randomizeButton').click()
            cy.wait(500)
            cy.get('#randomizedOutput').then(($randomizedDrink) => {
                console.log($randomizedDrink.text())
                let firstDrink = $randomizedDrink.text().split(':')[1].split(' ')[1];
                cy.get('#getstarted > div > div:nth-child(4) > div > div > ul').contains(firstDrink)
            })
        })
        it('The randomized drink is in the list after switch', function () {
            cy.get('#playlists > div > div > div:nth-child(4) > a > div').click()
            cy.get('#randomizeButton').click()
            cy.wait(500)
            cy.get('#randomizedOutput').then(($randomizedDrink) => {
                console.log($randomizedDrink.text())
                let firstDrink = $randomizedDrink.text().split(':')[1].split(' ')[1];
                cy.get('#getstarted > div > div:nth-child(4) > div > div > ul').contains(firstDrink)
            })
        })
    })
})