Feature: Login Functions

  As a bevrander
  I want to be able to login
  So that I can use all the functionality the site offers private users

  Scenario Outline: Logging in a user on <device>
    Given I am a registered user logging in using <device>
    When I enter my credentials and login
    Then I should be rerouted to the profile page
    And I should end up at my profile with my username filled out

    Examples:
      | device     |
      | iphone-6   |
      | ipad-2     |
      | macbook-15 |

  Scenario Outline: Logging in with bad credentials on <device> leads to a <errorText>
    # there is a bug here, email is not checked when logging in
    Given I am a registered user logging in using <device>
    When I log myself in using <username> and <email> and <password>
    Then I should get an error with the term <message> and <errorText>

    Examples:
      | device     | username    | email             | password    | message    | errorText    |
      | iphone-6   | nottestuser | test@admin.nl     | testuser    | went wrong | Login failed |
      | ipad-2     | ntestuser    | nottest@admin.nl | testuser    | went wrong | Login failed |
      | macbook-15 | testuser    | test@admin.nl     | nottestuser | went wrong | Login failed |