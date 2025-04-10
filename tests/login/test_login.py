import pytest
import os  # Keep os import if needed elsewhere, or remove if not
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from faker import Faker


@pytest.mark.smoke
@pytest.mark.login
def test_successful_login(page: Page, test_config: dict):
    """Tests successful login using credentials from the test_config fixture."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(test_config["username"], test_config["password"])

    # Add assertion for successful login, e.g., check for dashboard element or URL change
    expect(page, 
           message="User should be redirected to the dashboard after successful login").to_have_url("/dashboard")  # Example assertion
    # expect(page.locator("#user-profile")).to_be_visible()


@pytest.mark.regression
@pytest.mark.login
def test_failed_login_invalid_password(
    page: Page, faker_instance: Faker, test_config: dict
):
    """Tests failed login attempt with incorrect password generated by Faker."""
    login_page = LoginPage(page)
    invalid_password = faker_instance.password()
    real_username = test_config["username"]  # Use the real username from config

    login_page.navigate()
    login_page.login(real_username, invalid_password)

    # Add assertion for failed login
    error_message = login_page.get_error_message()
    expect(login_page.error_message).to_be_visible()
    assert error_message is not None
    assert "invalid credentials" in error_message.lower()  # Example error text check
