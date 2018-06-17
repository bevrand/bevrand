let userName = '';
let passWord = '';

describe('Page comes up', function () {
    it('.Visits the beverage randomizer', function () {
        cy.visit('http://0.0.0.0:4540')
        cy.title().should('eq', 'The Beverage Randomizer')
    })})

describe('Randomize functionality works', function () {
    it('.should be able to randomize my drinks', function () {
        cy.visit('http://0.0.0.0:4540')
        cy.get('#letsGetStartedButton').click()
        cy.get('#randomizeButton').click()
        cy.get('#randomizedOutput').contains('randomized')
    })
    it('.should be able to switch list', function () {
        cy.visit('http://0.0.0.0:4540')
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
    it('.The randomized drink is in the list', function () {
        cy.visit('http://0.0.0.0:4540')
        cy.get('#letsGetStartedButton').click()
        cy.get('#randomizeButton').click()
        cy.get('#randomizedOutput').then(($randomizedDrink) => {
            let firstDrink = $randomizedDrink.text().split(':')[1];
            console.log(firstDrink)
        })
    })
})

// describe('Register', function () {
//     it('.should be able to reach the register page', function () {
//         cy.visit('http://0.0.0.0:4540')
//         cy.get('#navbarResponsive > ul > li:nth-child(2) > a').click()
//         cy.url().should('eq', 'http://0.0.0.0:4540/register')
//     })

//     it('.should be able to register a user', function () {
//         userName = makeRandomString(15)
//         passWord = makeRandomString(10)

//         cy.get('#userName')
//         .type(userName).should('have.value', userName)
//         cy.get('#emailAddress')
//         .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
//         cy.get('#passWord')
//         .type(passWord).should('have.value', passWord)
//         cy.get('#controlPassWord')
//         .type(passWord).should('have.value', passWord)
//     })
// })

function makeRandomString(numberOfChars) {
    var text = ""
    var possible = "abcdefghijklmnopqrstuvwxyz0123456789"

    for (var i = 0; i < numberOfChars; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}