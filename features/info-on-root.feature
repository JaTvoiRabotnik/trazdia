Feature: showing off behave

  Scenario: run a simple test
     Given we have behave installed
      when we implement a test
      then behave will test it for us!


  Scenario: Access collector root

    Given any user
    When I access the path /collector
    Then I see the text "TrazDia: colletor de Diarios Oficials"
