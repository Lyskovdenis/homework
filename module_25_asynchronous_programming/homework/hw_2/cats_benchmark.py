import time
import asyncio
from pathlib import Path
import concurrent.futures

import aiohttp       # для асинхронного HTTP
import requests      # для тредов и процессов


# ------------- Настройки -------------

CATS_BASE = [
    "https://cdn.pixabay.com/photo/2016/02/10/16/37/cat-1192026_960_720.jpg",
    "https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720_960_720.jpg",
]

URLS_10 = CATS_BASE * 5          # 10 картинок
URLS_50 = CATS_BASE * 25         # 50 картинок
URLS_100 = CATS_BASE * 50        # 100 картинок

DOWNLOAD_DIR = Path("cats_bench")
DOWNLOAD_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0 Safari/537.36"
    )
}


def save_file(path: Path, data: bytes) -> None:
    """Синхронная запись файла через стандартный open."""
    with open(path, "wb") as f:
        f.write(data)


async def download_cat_async(session: aiohttp.ClientSession, url: str, filename: Path) -> None:
    try:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status != 200:
                return
            content = await resp.read()
    except aiohttp.ClientError:
        return

    loop = asyncio.get_running_loop()
    # асинхронная запись через run_in_executor
    await loop.run_in_executor(None, save_file, filename, content)


async def async_download_and_save(urls: list[str]) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            filename = DOWNLOAD_DIR / f"async_{i}.jpg"
            tasks.append(download_cat_async(session, url, filename))
        await asyncio.gather(*tasks)


def download_cat_thread(url: str, filename: Path) -> None:
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            return
        save_file(filename, resp.content)
    except requests.RequestException:
        return


def threaded_download(urls: list[str]) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        futures = []
        for i, url in enumerate(urls):
            filename = DOWNLOAD_DIR / f"thread_{i}.jpg"
            futures.append(ex.submit(download_cat_thread, url, filename))
        concurrent.futures.wait(futures)


def download_cat_process(url: str, filename_str: str) -> None:
    filename = Path(filename_str)
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            return
        save_file(filename, resp.content)
    except requests.RequestException:
        return


def process_download(urls: list[str]) -> None:
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as ex:
        futures = []
        for i, url in enumerate(urls):
            filename = str(DOWNLOAD_DIR / f"proc_{i}.jpg")
            futures.append(ex.submit(download_cat_process, url, filename))
        concurrent.futures.wait(futures)


def benchmark_one(name: str, urls: list[str]) -> tuple[int, float, float, float]:
    # Async
    t0 = time.perf_counter()
    asyncio.run(async_download_and_save(urls))
    t_async = time.perf_counter() - t0

    # Threads
    t0 = time.perf_counter()
    threaded_download(urls)
    t_threads = time.perf_counter() - t0

    # Processes
    t0 = time.perf_counter()
    process_download(urls)
    t_proc = time.perf_counter() - t0

    return (int(name), t_async, t_threads, t_proc)


def main() -> None:
    results = []
    results.append(benchmark_one("10", URLS_10))
    results.append(benchmark_one("50", URLS_50))
    results.append(benchmark_one("100", URLS_100))

    # Вывод для Markdown-таблицы
    print("| Кол-во картинок | Async (сек) | Threads (сек) | Processes (сек) |")
    print("|-----------------|------------:|--------------:|----------------:|")
    for images, t_async, t_threads, t_proc in results:
        print(f"| {images:<15} | {t_async:10.3f} | {t_threads:12.3f} | {t_proc:16.3f} |")


if __name__ == "__main__":
    main()