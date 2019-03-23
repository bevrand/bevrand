Feature: Randomizations
  As a bevrander
  I want to verify the randomize functionality
  So that we can safely deploy


  Scenario: Any drink from a random list
    Given we have a test environment
    When we request a random drink from the proxy
    Then we should get a status of '200' with a random drink

  Scenario: Random drink from specific list
    Given we have a test environment
    When we request all playlists
    And we randomize from 'tgif'
    Then we should get a random drink from that playlist

  Scenario: All private playlists should be randomizable
    Given we have a test environment
    And we request all playlists
    When I randomize from these playlists
    Then all playlists should give a result of '200'