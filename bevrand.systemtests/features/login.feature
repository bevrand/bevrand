Feature: Logging on
  As a bevrander
  I want to to be able to logon
  So that I can use the private functionality offered by this great website


  Scenario Outline: Login a new user using either email or username
    Given we have a test environment
    When we create a new user
    And we login this created user using <field>
    Then the result has <code> and a token attached

    Examples:
      | code | field        |
      | 200  | emailAddress |
      | 200  | username     |
