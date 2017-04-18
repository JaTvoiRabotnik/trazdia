from selenium import webdriver


def before_all(context):
    context.browser = webdriver.PhantomJS()
    context.browser.implicitly_wait(1)
    context.server_url = 'http://localhost:8000'


def after_all(context):
    context.browser.quit()
    context.browser = None

def before_feature(context, feature):
    # Code to be executed each time a feature is going to be tested
    pass
