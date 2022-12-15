import pytest
import param
from pages.auth_page import AuthPage
from pages.registration_page import RegPage
from delayed_assert import expect, assert_expectations


# Тест-кейс RTL-001 (Bug RTB-001)
@pytest.mark.xfail(reason="Таб выбора 'Номер' не соответсвует Требованиям")
def test_start_page(web_browser):
    """
    Главная страница сайта соответствует Требованиям по проекту.
    """
    page = AuthPage(web_browser)
    phone_tab_class = page.phone_tab.get_attribute("class")
    expect(page.auth_form.find(timeout=1))
    expect(page.lk_form.find(timeout=1))
    expect(phone_tab_class == "rt-tab rt-tab--small rt-tab--active")
    expect(page.phone.is_clickable())
    expect(page.password.is_clickable())
    expect(page.btn_login.is_clickable())
    expect(page.reg_link.is_clickable())
    expect(page.phone_tab.get_text() == "Номер")
    expect(page.auth_title.get_text() == "Авторизация")
    expect(page.logo_lk.get_text() == "Личный кабинет")
    expect(page.slogan_lk.get_text() == "Персональный помощник в цифровом мире Ростелекома")
    assert_expectations()


# Тест-кейс RTL-002
def test_mail_tab(web_browser):
    """
    Главная страница сайта.
    При вводе номера телефона/почты/логина/лицевого счета - таб выбора аутентификации меняется автоматически.
    Телефон -> Почта.
    """
    page = AuthPage(web_browser)
    page.phone.send_keys(param.email)
    page.password.click()
    mail_tab_class = page.mail_tab.get_attribute("class")
    assert mail_tab_class == "rt-tab rt-tab--small rt-tab--active"


# Тест-кейс RTL-003 (Bug RTB-002)
@pytest.mark.xfail(reason="При вводе Мобильного телефона в активированном табе 'Логин' - таб выбора аутентификации"
                          " не меняется автоматически.")
def test_login_tab_for_phone(web_browser):
    """
    Главная страница сайта.
    При вводе номера телефона/почты/логина/лицевого счета - таб выбора аутентификации меняется автоматически.
    Логин -> Телефон.
    """
    page = AuthPage(web_browser)
    page.login_tab.click()
    page.phone.send_keys(param.phone)
    page.password.click()
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert phone_tab_class == "rt-tab rt-tab--small rt-tab--active"


# Тест-кейс RTL-004
def test_auth_valid_phone(web_browser):
    """
    Главная страница сайта.
    Авторизации по номеру телефона (корректные данные)
    """
    page = AuthPage(web_browser)
    page.phone.send_keys(param.phone)
    page.password.send_keys(param.password)
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс RTL-005
def test_auth_incorrect_password(web_browser):
    """
    Главная страница сайта.
    Авторизации по номеру телефона (неверный пароль для входа)
    """
    page = AuthPage(web_browser)
    page.phone.send_keys(param.phone)
    page.password.send_keys(param.password2)
    page.btn_login.click()
    forgot_the_password = page.wrong_login_password.get_attribute("class")
    assert forgot_the_password == "rt-link rt-link--orange login-form__forgot-pwd login-form__forgot-pwd--animated"


# Тест-кейс RTL-006
def test_auth_empty_phone(web_browser):
    """
    Главная страница сайта.
    Авторизации по номеру телефона (пустое поле "Мобильный телефон")
    """
    page = AuthPage(web_browser)
    page.password.send_keys(param.password)
    page.btn_login.click()
    assert page.message_invalid_username.get_text() == "Введите номер телефона"


# Тест-кейс RTL-007 (Bug RTB-003)
@pytest.mark.xfail(reason="Пустое поле 'Пароль', отсутствует цветовая индикация кнопки Забыл пароль")
def test_auth_empty_password(web_browser):
    """
    Главная страница сайта.
    Авторизации по номеру телефона (пустое поле "Пароль")
    """
    page = AuthPage(web_browser)
    page.phone.send_keys(param.phone)
    page.btn_login.click()
    assert page.message_enter_password.get_text() == "Введите пароль"


# Тест-кейс RTL-008
def test_auth_valid_mail(web_browser):
    """
    Главная страница сайта.
    Авторизации по почте (корректные данные)
    """
    page = AuthPage(web_browser)
    page.mail_tab.click()
    page.email.send_keys(param.email)
    page.password.send_keys(param.password)
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()


# Тест-кейс RTL-009
def test_auth_mail_incorrect_password(web_browser):
    """
    Главная страница сайта.
    Авторизации по почте (неверный пароль для входа)
    """
    page = AuthPage(web_browser)
    page.mail_tab.click()
    page.email.send_keys(param.email)
    page.password.send_keys(param.password2)
    page.btn_login.click()
    forgot_the_password = page.wrong_login_password.get_attribute("class")
    assert forgot_the_password == "rt-link rt-link--orange login-form__forgot-pwd login-form__forgot-pwd--animated"


# Тест-кейс RTL-010
def test_auth_empty_mail(web_browser):
    """
    Главная страница сайта.
    Авторизации по почте (пустое поле "Электронная почта")
    """
    page = AuthPage(web_browser)
    page.mail_tab.click()
    page.password.send_keys(param.password)
    page.btn_login.click()
    assert page.message_invalid_username.get_text() == "Введите адрес, указанный при регистрации"


# Тест-кейс RTL-011 (Bug RTB-004)
@pytest.mark.xfail(reason="Пустое поле 'Пароль', отсутствует цветовая индикация кнопки Забыл пароль")
def test_auth_mail_empty_password(web_browser):
    """
    Главная страница сайта.
    Авторизации по почте (пустое поле "Пароль")
    """
    page = AuthPage(web_browser)
    page.mail_tab.click()
    page.email.send_keys(param.email)
    # page.password.send_keys(param.password2)
    page.btn_login.click()
    forgot_the_password = page.wrong_login_password.get_attribute("class")
    assert forgot_the_password == "rt-link rt-link--orange login-form__forgot-pwd login-form__forgot-pwd--animated"


# Тест-кейс RTL-012 (Bug RTB-005)
@pytest.mark.xfail(reason="Страница восстановления пароля не соответствует Требованиям")
def test_recover(web_browser):
    """
    Страница восстановления пароля соответствует Требованиям по проекту.
    """
    page = AuthPage(web_browser)
    page.wrong_login_password.click()
    expect(page.phone_tab.get_text() == "Номер")
    expect(page.mail_tab.get_text() == "Почта")
    expect(page.login_tab.get_text() == "Логин")
    expect(page.ls_tab.get_text() == "Лицевой счёт")
    expect(page.phone.is_visible())
    expect(page.captcha.is_visible())
    expect(page.captchares.is_clickable())
    expect(page.resetbtn.get_text() == "Продолжить")
    expect(page.resetback.get_text() == "Вернуться")
    assert_expectations()


# Тест-кейс RTL-014
def test_empty_captcha(web_browser):
    """
    Сценарий восстановления пароля по номеру телефона, пустое поле Captcha.
    """
    page = AuthPage(web_browser)
    page.wrong_login_password.click()
    page.phone.send_keys(param.phone)
    page.resetbtn.click()
    assert page.reseterror.get_text() == "Неверный логин или текст с картинки"


# Тест-кейс RTL-016 (Bug RTB-007)
@pytest.mark.xfail(reason="Название кнопки на равно 'Продолжить' и отсутствуют логотип/слоган Компании")
def test_reg_page_and_continue_button(web_browser):
    """
    Страница регистрации соответствует Требованиям по проекту.
    """
    auth_page = AuthPage(web_browser)
    auth_page.reg_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    expect(reg_page.name_field_text.get_text() == "Имя")
    expect(reg_page.last_name_field_text.get_text() == "Фамилия")
    expect(reg_page.region_field_text.get_text() == "Регион")
    expect(reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон")
    expect(reg_page.password_field_text.get_text() == "Пароль")
    expect(reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля")
    expect(reg_page.continue_button.get_text() == "Продолжить")
    expect(reg_page.logo_lk.get_text() == "Личный кабинет")
    expect(reg_page.slogan_lk.get_text() == "Персональный помощник в цифровом мире Ростелекома")
    assert_expectations()


# Тест-кейс RTL-017
def test_reg_incorrect_name(web_browser):
    """
    Страница регистрации, ввод некорректных данных (Имя или Фамилия состоит из 1 буквы)
    """
    auth_page = AuthPage(web_browser)
    auth_page.reg_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.min_name)
    reg_page.last_name_field.send_keys(param.min_lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс RTL-018
def test_reg_latin_chars(web_browser):
    """
    Страница регистрации, ввод некорректных данных (Имя или Фамилия  написано латиницей)
    """
    auth_page = AuthPage(web_browser)
    auth_page.reg_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.l_name)
    reg_page.last_name_field.send_keys(param.l_lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. " \
                                                                     "От 2 до 30 символов."


# Тест-кейс RTL-019
def test_reg_name_max_chars(web_browser):
    """
    Страница регистрации, ввод некорректных данных (Имя и Фамилия  состоит из 31 буквы)
    """
    auth_page = AuthPage(web_browser)
    auth_page.reg_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.max_name)
    reg_page.last_name_field.send_keys(param.max_lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс RTL-020
def test_reg_incorrect_password(web_browser):
    """
    Страница регистрации, ввод пароля меньше 8ми символов (5)
    """
    auth_page = AuthPage(web_browser)
    auth_page.reg_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.fail_password)
    reg_page.password_confirmation_field.send_keys(param.fail_password)
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"


# Тест-кейс RTL-021 (Bug RTB-008)
@pytest.mark.xfail(reason="Отсутствует Кнопка 'Закрытия всплывающего окна'")
def test_reg_with_email_registered_user(web_browser):
    """
    Страница регистрации, ввод E-mail уже зарегистрированного в системе.
    """
    auth_page = AuthPage(web_browser)
    auth_page.reg_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.email)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password)
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'


# Тест-кейс RTL-022 (Bug RTB-009)
@pytest.mark.xfail(reason="Кнопки 'Зарегистрироваться' и 'Отмена' не соответствуют Требованиям по проекту.")
def test_reg_with_phone_registered_user(web_browser):
    """
    Страница регистрации, ввод Телефона уже зарегистрированного в системе.
    """
    auth_page = AuthPage(web_browser)
    auth_page.reg_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys(param.name)
    reg_page.last_name_field.send_keys(param.lastname)
    reg_page.email_or_mobile_phone_field.send_keys(param.phone)
    reg_page.password_field.send_keys(param.password)
    reg_page.password_confirmation_field.send_keys(param.password)
    reg_page.continue_button.click()
    expect(reg_page.notification_form.is_visible)
    expect(reg_page.login_button.get_text() == 'Зарегистрироваться')
    expect(reg_page.recover_password_button.get_text() == 'Отмена')
    assert_expectations()
