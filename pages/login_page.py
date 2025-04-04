from playwright.sync_api import Page
from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object for a hypothetical Login Page."""
    ENDPOINT = "/login.htm"

    @property
    def username_input(self):
        return self.page.locator("#username")

    @property 
    def password_input(self):
        return self.page.locator("#password")

    @property
    def login_button(self):
        return self.page.locator("button[type='submit']")

    @property
    def error_message(self):
        return self.page.locator(".error-message")  # Example error locator

    def login(self, username: str, password: str) -> None:
        """Fills the login form and submits it."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str | None:
        """Gets the text content of the error message element, if visible."""
        if self.error_message.is_visible():
            return self.error_message.text_content()
        return None

