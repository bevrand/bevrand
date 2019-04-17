Feature: Register Functions

  As a bevrander
  I want to be able to register
  So that I can use all the functionality the site offers private users

  @focus
  Scenario Outline: Creating a new user on <device>
    Given I am a registering user using <device>
    When I register myself as a new user
    Then I should be rerouted to the reroute page
    And I should end up at my profile with my username filled out

    Examples:
      | device     |
      | iphone-6   |
      | ipad-2     |
      | macbook-15 |

