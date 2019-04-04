Feature: Highscores
  As a bevrander
  I want to to be able to receive highscores
  So that I can join the global community

  Scenario: Getting global highscores
    Given we have a test environment
    When we ask for the global highscore
    Then we should get a result of '200'