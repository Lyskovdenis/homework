import asyncio
from pathlib import Path

import aiohttp  # HTTP-клиент, его оставляем


# Список URL с картинками котов.
CATS = [
    "https://cdn.pixabay.com/photo/2016/02/10/16/37/cat-1192026_960_720.jpg",
    "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_960_720.jpg",
    "https://cdn.pixabay.com/photo/2017/09/16/19/49/cat-2754330_960_720.jpg",
]

DOWNLOAD_DIR = Path("cats")
DOWNLOAD_DIR.mkdir(exist_ok=True)


# Заголовки, чтобы выглядеть как обычный браузер
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0 Safari/537.36"
    )
}


def save_file(path: Path, data: bytes) -> None:
    """
    Синхронная функция записи файла.
    Здесь используется только стандартный open, без aiofiles.
    """
    with open(path, "wb") as f:
        f.write(data)


async def async_save_file(path: Path, data: bytes) -> None:
    """
    Асинхронная обёртка: выполняет save_file в пуле потоков,
    чтобы не блокировать event loop.
    """
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, save_file, path, data)


async def download_cat(session: aiohttp.ClientSession, url: str) -> None:
    filename = DOWNLOAD_DIR / url.split("/")[-1]

    try:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status != 200:
                print(f"Не удалось скачать {url}: статус {resp.status}")
                return

            content = await resp.read()
    except aiohttp.ClientError as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return

    # Сохранение файла асинхронно через стандартный open
    await async_save_file(filename, content)
    print(f"Сохранён файл: {filename}")


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        tasks = [download_cat(session, url) for url in CATS]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())