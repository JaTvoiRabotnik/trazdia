from behave import given, when, then

@given('an anonymous request')
def step_impl(context):
    pass

@when('I ask for the index for a DO')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/collector/Diario_Oficial_SP/20170207')

    # Checks for Cross-Site Request Forgery protection input
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()


@then('I receive a list of links to the pages of the DO')
def step_impl(context):
    br = context.browser

    # Checks that we get a JSON file
    
