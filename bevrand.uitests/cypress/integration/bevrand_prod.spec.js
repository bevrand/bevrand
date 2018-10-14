let userName = '';
let passWord = '';

context('Beverage Randomizer Test', () => {
    beforeEach(() => {
        cy.visit('https://www.beveragerandomizer.com')
    })

describe('Page comes up', function () {
    it('Visits the beverage randomizer', function () {
        cy.title().should('eq', 'The Beverage Randomizer')
    })})
})