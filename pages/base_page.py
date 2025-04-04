from playwright.sync_api import Page


class BasePage:
    """Base class for all Page Objects."""
    ENDPOINT: str | None = None

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str | None = None):
        """Navigates the page to the specified URL.
        If no URL is provided, it will use the ENDPOINT property."""
        if url is None:
            url = self.ENDPOINT
        if url is None and self.ENDPOINT is None and self.page.base_url:
            raise ValueError("No URL provided and no base URL found")
        self.page.goto(url, wait_until="load")

    def wait(self, millis: int):
        """Pauses execution for the specified number of milliseconds.
        This method is the recommended way to add delays in tests instead of time.sleep(),
        as it integrates properly with Playwright's timing system."""
        self.page.wait_for_timeout(millis)
