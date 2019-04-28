Feature: Playlists
  As a bevrander
  I want to to be able to manage my own playlists
  So that I can start randomizing my own lists

  Scenario Outline: Creating a new user playlist
    Given We create <user> with <email>
    When we create a <user> user based <playlist>
    Then we should get a result of <code>

    Examples:
      | user                | email                        | playlist     | code |
      | creatingnewplaylist | creatingnewplaylist@email.nl | someplaylist | 201  |
      | frontpage           | playlistfrontpage@email.nl   | someplaylist | 403  |
      | global              | playlistglobal@email.nl      | someplaylist | 403  |

  Scenario Outline: Creating a new user playlist and retrieving it
    Given We create <user> with <email>
    When we create a <user> user based <playlist>
    And we create a <user> user based <secondPlaylist>
    Then we should be able to retrieve <user> playlists
    And the number of returned playlists should be <number_of_lists>
    And we should get a result of <code>

    Examples:
      | user                  | email                          | playlist     | secondPlaylist    | code | number_of_lists |
      | retrievingnewplaylist | retrievingnewplaylist@email.nl | someplaylist | someotherplaylist | 201  | 2               |

  Scenario Outline: Deleting all playlists for a user
    Given We create <user> with <email>
    When we create a <user> user based <playlist>
    And we create a <user> user based <secondPlaylist>
    And we delete all playlists for <user>
    Then we should get a result of <code>
    And we should be able to retrieve <user> playlists
    And the number of returned playlists should be <number_of_lists>

    Examples:
      | user                | email                        | playlist     | secondPlaylist    | code | number_of_lists |
      | deletingnewplaylist | deletingnewplaylist@email.nl | someplaylist | someotherplaylist | 204  | 0               |

  Scenario Outline: Updating a playlist
    Given We create <user> with <email>
    When we create a <user> user based <playlist>
    And we update a <user> user based <playlist>
    Then we should get a result of <code>
    And we should be able to retrieve <user> playlists
    And the number of returned playlists should be <number_of_lists>
    And the <field> should be updated to <updated>

    Examples:
      | user               | email                        | playlist            | code | number_of_lists | field       | updated                     |
      | updateningplaylist | updatingnewplaylist@email.nl | someupdatedplaylist | 204  | 1               | displayName | I am no longer so depressed |

