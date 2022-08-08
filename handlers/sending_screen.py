import io
from logger import logger
from arsenic import services, browsers
from arsenic import get_session
import PIL.Image as Image


async def make_screen(url, date_request, user_id, domen):

    # Initialize Chrome webrdiver
    service = services.Chromedriver()
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]}
    }

    async with get_session(service, browser) as session:
        await session.get(url)
        await session.set_window_size(1024, 1460)
        screen = await session.get_screenshot()

    img = Image.open(io.BytesIO(screen.read()))
    img.save(f"{date_request}_{user_id}_{domen}.png")

    screen.seek(0)