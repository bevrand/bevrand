Feature: Highscores
  As a bevrander
  I want to to be able to receive highscores
  So that I can join the global community

  Scenario Outline: Getting global highscores
    Given we have randomized a few times
    When we query the global highscore
    Then we should get a result of <code>
    Examples:
    | code |
    | 200  |

  Scenario Outline: Getting frontpage highscores
    Given we have randomized a few times
    When we query the <frontpage> and <playlist> highscore
    Then we should get a result of <code>
    Examples:
      | frontpage | playlist      | code |
      | frontpage | tgif          | 200  |
      | frontpage | officemadness | 200  |
      | frontpage | girlsnightout | 200  |

  Scenario Outline: Getting user highscores
    Given We create <user> with <email>
    When we create a <user> user based <playlist>
    And we randomize as <user> for <playlist>
    And we query the <user> and <playlist> highscore
    Then we should get a result of <code>
    Examples:
      | user              | email                           | playlist | code |
      | bevrandhighscorer | bevrandhighscorer@systemtest.nl | bevrand  | 200  |
