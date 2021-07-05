from selenium import webdriver


def Chrome():
    """ Launch chrome selenium webdriver with headless option. """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(chrome_options=options)


def Firefox():
    """ Launch firefox selenium webdriver with headless option. """
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(firefox_options=options)
