Feature: Playlists
  As a bevrander
  I want to to be able to manage my own playlists
  So that I can start randomizing my own lists

  Scenario Outline: Creating a new user playlist
    Given <user> with <email> does not exist
    When we create a <user> user based <playlist>
    Then we should get a result of <code>

    Examples:
      | user      | email                      | playlist   | code |
      | test      | playlisttest@email.nl      | someplaylist | 201  |
      | frontpage | playlistfrontpage@email.nl |someplaylist | 403  |
      | global    | playlistglobal@email.nl |someplaylist | 403  |

  Scenario Outline: Creating a new user playlist and retrieving it
    Given <user> with <email> does not exist
    When we create a <user> user based <playlist>
     And we create a <user> user based <secondPlaylist>
    Then we should be able to retrieve <user> playlists
     And the number of returned playlists should be <number_of_lists>
     And we should get a result of <code>

    Examples:
      | user | email | playlist     | secondPlaylist    | code | number_of_lists |
      | test | playlisttest@email.nl      | someplaylist | someotherplaylist | 200  | 2               |

  Scenario Outline: Deleting all playlists for a user
    Given <user> with <email> does not exist
    When we create a <user> user based <playlist>
    And we create a <user> user based <secondPlaylist>
    And we delete all playlists for <user>
    Then we should get a result of <code>
    And we should be able to retrieve <user> playlists
    And the number of returned playlists should be <number_of_lists>

    Examples:
      | user | email |playlist     | secondPlaylist    | code | number_of_lists |
      | test | playlisttest@email.nl|someplaylist | someotherplaylist | 204  | 0               |
