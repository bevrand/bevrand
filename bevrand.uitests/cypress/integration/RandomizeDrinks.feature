Feature: Randomizer Functions

  As a bevrander
  I want to be able to Randomize beverages
  Since that is what the site is called

  Scenario Outline: Selecting any list with <device> and press Randomize
    Given I am a new user using <device>
    When I select any playlist
    And I randomize a drink
    Then I should get a result

    Examples:
      | device     |
      | iphone-6   |
      | ipad-2     |
      | macbook-15 |

  Scenario Outline: Randomized drink should be in the selected playlist
    Given I am a new user using <device>
    When I select a playlist and view the detail page
    And I randomize a drink
    Then the result should be in the beveragelist from the detail page

    Examples:
      | device     |
      | iphone-6   |

  Scenario Outline: Randomized drink should be in the selected playlist after switching
    Given I am a new user using <device>
    When I select a playlist and view the detail page
    And I randomize a drink
    And I select a playlist and view the detail page
    And I randomize a drink
    Then the result should be in the beveragelist from the detail page

    Examples:
      | device     |
      | macbook-15 |