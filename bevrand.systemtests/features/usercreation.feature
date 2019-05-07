Feature: UserCreation
  As a bevrander
  I want to to be able to create a new unique user
  So that I can use the functionality offered by this great website


  Scenario Outline: Create a sample user
    Given we have a test environment
    When we create a new user
    Then we should get a result of <code>

  Examples:
    | code |
    | 200  |
