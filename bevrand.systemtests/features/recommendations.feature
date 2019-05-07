Feature: Recommendations
  As a bevrander
  I want to to be able to receive recommendations
  So that I can better choose which drink I want to consume

  Scenario: Getting groups of beverages
    Given we have a test environment
    When we ask for a grouped recommendation
    Then we skip this code for now