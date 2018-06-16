var userName = "";
var passWord = "";

describe('Page is up', function () {
    it('.should() - assert that <title> is correct', function () {
      //cy.visit('https://beveragerandomizer.com/')
      cy.visit('http://0.0.0.0:4540')
      cy.title().should('include', 'The Beverage Randomizer')
    })})

describe('Buttons scroll down', function () {
  it('.should() - assert that buttons scrolls down', function () {
   // cy.visit('https://beveragerandomizer.com/')
    cy.visit('http://0.0.0.0:4540')
    cy.get('#letsGetStartedButton').click()
  })
  it('.should be able to randomize a drink', function () {
      cy.get('#randomizeButton').click()
  })
})

describe('Register', function () {
  it('.should be able to reach the register page', function () {
    cy.visit('http://0.0.0.0:4540/')
    cy.get('#navbarResponsive > ul > li:nth-child(2) > a').click()
    cy.url().should('eq', 'http://0.0.0.0:4540/register')
  })

  it('.should be able to register a user', function () {
    userName = makeRandomString(15)
    passWord = makeRandomString(10)

  cy.get('#emailAddress')
  .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
  cy.get('#userName')
  .type(userName).should('have.value', userName)
  cy.get('#passWord')
  .type(passWord).should('have.value', passWord) 
  cy.get('#controlPassWord')
  .type(passWord).should('have.value', passWord) 
  cy.get('#root > div > div > span > div > form > button').click()  
  cy.url().should('eq', 'http://0.0.0.0:4540/login')
})
it('.should be able to login a user', function () {
  cy.get('#emailAddress')
  .type(`${userName}@email.com`).should('have.value', `${userName}@email.com`)
  cy.get('#userName')
  .type(userName).should('have.value', userName)
  cy.get('#passWord')
  cy.get('#passWord')
  .type(passWord).should('have.value', passWord) 
  cy.get('#root > div > div > span > div > form > button > i').click()
  cy.url().should('eq', 'http://0.0.0.0:4540/user')
})
})

function makeRandomString(length) {
  var text = "";
  var possible = "abcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < length; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}