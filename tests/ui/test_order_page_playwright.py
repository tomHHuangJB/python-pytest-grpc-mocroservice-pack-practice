import pytest

from order_app.api import create_app
from order_app.repository import InMemoryOrderRepository
from order_app.service import OrderService
from tests.helpers.inventory import ApiInventoryStub
from tests.helpers.server import run_app_server


def _open_browser():
    playwright = pytest.importorskip("playwright.sync_api")
    api = playwright.sync_playwright().start()
    try:
        browser = api.chromium.launch()
    except Exception as exc:
        api.stop()
        pytest.skip(f"Playwright browser is not installed: {exc}")
    return api, browser


@pytest.mark.ui
def test_order_page_creates_order_and_shows_confirmation() -> None:
    repository = InMemoryOrderRepository()
    inventory = ApiInventoryStub(mode="ok")
    service = OrderService(repository=repository, inventory_client=inventory, id_factory=lambda: "ui-order-001")
    app = create_app(order_service=service)

    with run_app_server(app) as base_url:
        api, browser = _open_browser()
        page = browser.new_page()
        try:
            page.goto(base_url)
            page.locator("#submit-order").click()
            expect = pytest.importorskip("playwright.sync_api").expect
            expect(page.locator("#result")).to_contain_text("Order ui-order-001 created")
            assert repository.count() == 1
        finally:
            browser.close()
            api.stop()


@pytest.mark.ui
def test_order_page_surfaces_downstream_errors() -> None:
    repository = InMemoryOrderRepository()
    inventory = ApiInventoryStub(mode="out_of_stock")
    service = OrderService(repository=repository, inventory_client=inventory)
    app = create_app(order_service=service)

    with run_app_server(app) as base_url:
        api, browser = _open_browser()
        page = browser.new_page()
        try:
            page.goto(base_url)
            page.locator("#sku").fill("sku-out")
            page.locator("#submit-order").click()
            expect = pytest.importorskip("playwright.sync_api").expect
            expect(page.locator("#result")).to_contain_text("Error 409: inventory unavailable")
            assert repository.count() == 0
        finally:
            browser.close()
            api.stop()
