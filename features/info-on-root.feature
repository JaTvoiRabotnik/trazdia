Feature: Info in Root

  Scenario: Access collector root

    Given any user
    When I access the path /collector
    Then I see the text "TrazDia: colletor de Diarios Oficials"
