from pages.login_page import LoginPage

def test_login_exitoso(driver):
    login = LoginPage(driver)
    login.open()
    login.login_workflow("NCRUZV", "Clave123")
    