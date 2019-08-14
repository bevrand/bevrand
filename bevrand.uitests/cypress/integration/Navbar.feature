Feature: Navbar

  As a bevrander
  I want to be make sure the navbar can be seen and interacted with on every page

  Scenario Outline: Navbar is shown on each page using <device>
    Given I am a new user using <device>
     When I visit the page <page>
      And I open the navbar menu
     Then The navbar should be visible and usable

    Examples:
      | device     | page                    |
      | iphone-6   | /                       |
      | ipad-2     | register                |
      | macbook-15 | login                   |
      | iphone-6   | profile                 |
      | ipad-2     | reroute/test            |
      | macbook-15 | playlistcreation/Asfasf |

  Scenario: Logged off status is shown
    Given I am a new user using macbook-15
     When I open the navbar menu
     Then The logged off status should be shown

  Scenario: Logged on status is shown
    Given I am a registered user logging in using iphone-6
     When I enter my credentials and login
     Then The logged on status should be shown

  Scenario: Logged off status is shown after logging out
    Given I am a registered user logging in using ipad-2
     When I enter my credentials and login
     When I press logout on the navbar
     Then The logged off status should be shown
      And I should be rerouted to the login page
