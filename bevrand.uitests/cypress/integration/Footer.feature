Feature: Footer

  As a bevrander
  I want to be make sure the footer can be seen and interacted with on every page

  Scenario Outline: Footer is shown on each page using <device>
    Given I am a new user using <device>
    When I visit the page <page>
    Then The footer should be visible and usable

    Examples:
      | device     | page                    |
      | iphone-6   | /                       |
      | ipad-2     | register                |
      | macbook-15 | login                   |
      | iphone-6   | profile                 |
      | ipad-2     | reroute/test            |
      | macbook-15 | playlistcreation/Asfasf |
      | macbook-15 | playlistdetails         |
