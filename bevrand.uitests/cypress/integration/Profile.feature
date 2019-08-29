Feature: Profile

  As a bevrander
  I want to be able to go to my profile page
  So that I can do admin tasks for my profile

  Scenario Outline: Creating a playlist on <device>
    Given I am a registered user logging in using <device>
    When I enter my credentials and login
    When I arrive at my profile
    And I click on the add playlist button
    And I choose a random name as my playlist name
    And I click <button>
    And I get the time to get some drinks alert when pressing <button>
    Then I should be rerouted to the <page> page

    Examples:
      | device     | button | page             |
      | iphone-6   | cancel | profile          |
      | ipad-2     | create | playlistcreation |
      | macbook-15 | cancel | profile          |

  Scenario Outline: Creating a playlist complete flow happy path on <device>
    Given I am a registered user logging in using <device>
    When I enter my credentials and login
    When I arrive at my profile
    And I click on the add playlist button
    And I choose a random name as my playlist name
    And I click <button>
    And I get the time to get some drinks alert when pressing <button>
    And I add a few valid drinks in the playlistcreation screen
    And I save this playlist
    Then I should get a validation of success
    And I should be rerouted to the <page> page
    And My new playlist should be visible
    Examples:
      | device     | button | page    |
      | macbook-15 | create | profile |

  Scenario Outline: Cannot create playlist twice <device>
    Given I am a registered user logging in using <device>
    When I enter my credentials and login
    When I arrive at my profile
    And I click on the add playlist button
    And I choose add the preseeded playlist
    And I click <button>
    Then I should get an error with the text <errorText>
    And I should be rerouted to the <page> page

    Examples:
      | device   | button | page    | errorText      |
      | iphone-6 | create | profile | already exists |

  Scenario Outline: Selecting and playing a playlist on <device> should reroute
    Given I am a registered user logging in using <device>
    When I enter my credentials and login
    When I arrive at my profile
    And I select the dice to play the playlist
    Then I should be rerouted to the homepage with anchor <anchor>
    And the selected playlist should be <name>

    Examples:
      | device     | anchor | name              |
      | macbook-15 | main   | I am so depressed |
