Feature: Highscores
  As a bevrander
  I want to to be able to receive highscores
  So that I can join the global community

  Scenario: Getting global highscores
    Given we have randomized a few times
    When we query the global highscore
    Then we should get a result of '200'

  Scenario Outline: Getting frontpage highscores
    Given we have randomized a few times
    When we query the <frontpage> and <playlist> highscore
    Then we should get a result of '200'
    Examples:
      | frontpage | playlist      |
      | frontpage | tgif          |
      | frontpage | officemadness |
      | frontpage | girlsnightout |

  Scenario Outline: Getting user highscores
    Given <user> does not exist
    When we create a <user> user based <playlist>
    And we randomize as <user> for <playlist>
    And we query the <user> and <playlist> highscore
    Then we should get a result of '200'
    Examples:
      | user      | playlist      |
      | bevrand   | bevrand       |

