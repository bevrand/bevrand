Feature: Detail page

  As a bevrander
  I want to be able to see more details regarding playlists
  So that I can see all drinks

  Scenario Outline: A playlist has more details on the detail page on <device>
    Given I am a new user using <device>
    When I click on more details for the playlist with position <position>
    Then I should be rerouted to the details page
    And I should see a list with <drinks> drinks
    Examples:
      | device     | drinks | position |
      | iphone-6   | 11     | 1        |
      | ipad-2     | 11     | 1        |
      | macbook-15 | 11     | 1        |

  Scenario Outline: A playlist can be selected using the detail page on <device>
    Given I am a new user using <device>
    When I click on more details for the playlist with position <position>
    And I click the dice icon to select the playlist
    Then I should be rerouted to the homepage with anchor <anchor>
    And the selected playlist should be <name>
    Examples:
      | device     | anchor | position | name           |
      | iphone-6   | main   | 3        | Mancave Mayhem |
      | ipad-2     | main   | 3        | Mancave Mayhem |
      | macbook-15 | main   | 3        | Mancave Mayhem |
