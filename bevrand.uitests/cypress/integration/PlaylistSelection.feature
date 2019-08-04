Feature: Playlist Selection

  As a bevrander
  I want to be able to choose playlists
  So that I do not have to think about my beverage choices

  Scenario Outline: Selecting a frontend playlist with <device>
    Given I am a new user using <device>
    When I select the first playlist by image
    Then The headertext matches the selected playlist

    Examples:
      | device     |
      | iphone-6   |
      | ipad-2     |
      | macbook-15 |

  Scenario Outline: Switching playlists with <device>
    Given I am a new user using <device>
    When I select the first playlist by image
    And I select another playlist by image
    Then The headertext matches the secondly selected playlist
    And The headertext does not match the first selected playlist

    Examples:
      | device     |
      | iphone-6   |
      | macbook-15 |

  Scenario Outline: Pagination changes on <device>
    Given I am a new user using <device>
    When I swipe to the next page
    Then The active first slide should not be the active slide

    Examples:
      | device     |
      | iphone-6   |
      | macbook-15 |

  Scenario Outline: Last playlist leads to login page on <device>
    Given I am a new user using <device>
    When I select the last playlist
    Then I should be rerouted to the login page

    Examples:
      | device     |
      | iphone-6   |
      | ipad-2     |
      | macbook-15 |
