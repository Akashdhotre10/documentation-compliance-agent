from pathlib import Path


class ScreenshotManager:

    def __init__(self, page):

        self.page = page

    def capture(self, filename):

        Path("data/screenshots").mkdir(
            exist_ok=True,
            parents=True
        )

        path = f"data/screenshots/{filename}.png"

        self.page.screenshot(
            path=path,
            full_page=True
        )

        print(f"Saved {path}")

        return path