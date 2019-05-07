Feature: Randomizations
  As a bevrander
  I want to verify the randomize functionality
  So that we can safely deploy

  Scenario Outline: Any drink from a random list
    Given we have a test environment
    When we request a random drink from the proxy
    Then we should get a status of <code> with a random drink
    Examples:
    | code |
    | 200  |

  Scenario Outline: Random drink from specific list
    Given we have a test environment
    When we request all playlists
    And we randomize from <playlist>
    Then we should get a random drink from that playlist
    Examples:
    | playlist |
    | tgif     |

  Scenario Outline: All public playlists should be randomizable
    Given we have a test environment
    And we request all playlists
    When I randomize from these playlists
    Then all playlists should give a result of <code>
    Examples:
      | code |
      | 200  |

  Scenario Outline: All private playlists should be randomizable
    Given we have a test environment
    And We create <user> with <email>
    When we create a <user> user based <playlist>
    And we randomize as <user> for <playlist>
    Then all playlists should give a result of <code>
    Examples:
      | code | user                   | email                      | playlist          |
      | 200  | privaterandomizinguser | privaterandomizing@user.nl | systemtestprivate |