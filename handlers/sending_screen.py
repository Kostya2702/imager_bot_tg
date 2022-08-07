from logger import logger
from selenium import webdriver


async def make_screen(url, date_request, user_id, domen):

    # Initialize Chrome webrdiver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
    except Exception:
        if __name__ == '__main__':
            logger.exception('InvalidArgumentException')

    # Setting up display size
    driver.set_window_size(1024, 1460)
    driver.maximize_window()

    # Makes screenshot
    driver.get_screenshot_as_file(f"{date_request}_{user_id}_{domen}.png")

    # Ending driver work
    driver.quit()