Feature: Register Functions

  As a bevrander
  I want to be able to register
  So that I can use all the functionality the site offers private users

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

  Scenario Outline: Field validation for <username>, <email>, <password> on <device>
    Given I am a registering user using <device>
    When I register myself using <username> and <email> and <password> and <repeatpassword>
    Then I should get an error with the term <message> and <errorText>

    Examples:
      | device     | username                              | email                 | password                                                     | repeatpassword                                               | message    | errorText                  |
      | iphone-6   | thisisaninvaliduserbecauseitistoolong | thisisavalid@email.nl | validpassword                                                | validpassword                                                | went wrong | Username should be between |
      | ipad-2     | u                                     | thisisavalid@email.nl | validpassword                                                | validpassword                                                | went wrong | Username should be between |
      | macbook-15 | " "                                   | thisisavalid@email.nl | validpassword                                                | validpassword                                                | went wrong | Username should be between |
      | macbook-15 | thisisavaliduser                      | thisisavalid@email    | validpassword                                                | validpassword                                                | went wrong | not a valid emailaddres    |
      | iphone-6   | thisisavaliduser                      | thisisavalid@email.nl | validpassword                                                | thispasswordisdifferent                                      | went wrong | Passwords do not match     |
      | ipad-2     | thisisavaliduser                      | thisisavalid@email.nl | invalidpasswordinvalidpasswordinvalidpasswordinvalidpassword | invalidpasswordinvalidpasswordinvalidpasswordinvalidpassword | went wrong | Password should be between |
      | macbook-15 | thisisavaliduser                      | thisisavalid@email.nl | p                                                            | p                                                            | went wrong | Password should be between |
      | iphone-6   | testuser                              | thisisavalid@email.nl | validpassword                                                | validpassword                                                | went wrong | Username already exists    |
      | macbook-15 | thisisavaliduser                      | test@admin.nl         | validpassword                                                | validpassword                                                | went wrong | Email already exists       |

  Scenario Outline: Field validation for email <email> in <device>
    Given I am a registering user using <device>
    When I register myself using <username> and <email> and <password> and <repeatpassword>
    Then I should not be rerouted to the reroute page

    Examples:
      | device   | username         | email                | password      | repeatpassword |
      | iphone-6 | thisisavaliduser | thisisavalidemail.nl | validpassword | validpassword  |
