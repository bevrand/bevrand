let userName = '';
let passWord = '';

context('Beverage Randomizer Test', () => {
    beforeEach(() => {
        cy.visit('http://0.0.0.0')
    }),

describe('Page comes up', function () {
    it('Visits the beverage randomizer', function () {
        cy.title().should('eq', 'The Beverage Randomizer')
    })})

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

describe('Register', function () {
    it('Should be able to reach the register page', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(2) > a').click()
        cy.url().should('eq', 'http://0.0.0.0/register')
    })

    it('Should be able to register a user', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(2) > a').click()
        userName = makeRandomString(15)
        passWord = makeRandomString(10)

        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#controlPassWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button > i').click()
        cy.url().should('eq', 'http://0.0.0.0/login')
    })
    it('Should not be able to register a user twice', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(2) > a').click()
        userName = makeRandomString(15)
        passWord = makeRandomString(10)

        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#controlPassWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/login')
        cy.get('#navbarResponsive > ul > li:nth-child(5) > a').click()
        cy.get('#navbarResponsive > ul > li:nth-child(2) > a').click()
        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#controlPassWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/register')

    })
})

describe('Login', function () {
    it('Should be able to reach the login page', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(1) > a').click()
        cy.url().should('eq', 'http://0.0.0.0/login')
    })
    it('Should be able to login a created user', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(1) > a').click()

        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/user')
        cy.get('#navbarResponsive > ul > li:nth-child(5) > a').click()
    })
    it('Should not be able to login with wrong password', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(1) > a').click()

        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        let wrongPassword = 'notthepassword'
        cy.get('#passWord')
        .type(wrongPassword).should('have.value', wrongPassword)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/login')
    })
    it('Should not be able to login with wrong username', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(1) > a').click()
        let wrongUsername = 'nottheusername'
        cy.get('#userName')
        .type(wrongUsername).should('have.value', wrongUsername)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/login')
    })
})

describe('Create', function () {
    it('Should be able to create a list', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(1) > a').click()

        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/user')
        cy.get('#navbarResponsive > ul > li:nth-child(4) > a').click()
        cy.url().should('eq', 'http://0.0.0.0/create')
       
        let listName = makeRandomString(10)
        let beverages = 'beer, wine, whiskey, whisky'

        cy.get('#displayName')
        .type(listName).should('have.value', listName)
        cy.get('#beverages')
        .type(beverages).should('have.value', beverages)
        cy.get('#playlistCreator > div > div > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/user')
    })
    it('Should not be able to post a list a name', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(1) > a').click()

        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/user')
        cy.get('#navbarResponsive > ul > li:nth-child(4) > a').click()
        cy.url().should('eq', 'http://0.0.0.0/create')
       
        let beverages = 'beer, wine, whiskey, whisky'

        cy.get('#beverages')
        .type(beverages).should('have.value', beverages)
        cy.get('#playlistCreator > div > div > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/create')
    })
    it('Should not be able to post a list without drinks', function () {
        cy.get('#navbarResponsive > ul > li:nth-child(1) > a').click()

        cy.get('#userName')
        .type(userName).should('have.value', userName)
        cy.get('#emailAddress')
        .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
        cy.get('#passWord')
        .type(passWord).should('have.value', passWord)
        cy.get('#root > div > div > span > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/user')
        cy.get('#navbarResponsive > ul > li:nth-child(4) > a').click()
        cy.url().should('eq', 'http://0.0.0.0/create')
       
        let listName = makeRandomString(10)

        cy.get('#displayName')
        .type(listName).should('have.value', listName)
        cy.get('#playlistCreator > div > div > div > form > button').click()
        cy.url().should('eq', 'http://0.0.0.0/create')
    })
})

function makeRandomString(numberOfChars) {
    let text = ""
    let possible = "abcdefghijklmnopqrstuvwxyz0123456789"

    for (let i = 0; i < numberOfChars; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
    
}
})

