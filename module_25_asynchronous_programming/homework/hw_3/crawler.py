import asyncio
from pathlib import Path
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup


class AsyncCrawler:
    def __init__(self, max_depth: int = 3, output_file: str = "links.txt"):
        self.max_depth = max_depth
        self.output_path = Path(output_file)
        self.seen_urls: set[str] = set()
        self.external_urls: set[str] = set()

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str | None:
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                return await resp.text()
        except aiohttp.ClientError:
            return None

    def extract_links(self, html: str, base_url: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        links: list[str] = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Приводим относительные ссылки к абсолютным
            full_url = urljoin(base_url, href)
            links.append(full_url)

        return links

    def is_external(self, url: str, root_domain: str) -> bool:
        parsed = urlparse(url)
        if not parsed.scheme.startswith("http"):
            return False
        return parsed.netloc and parsed.netloc != root_domain

    async def crawl(self, start_urls: list[str]) -> None:
        # очищаем прошлые результаты
        self.seen_urls.clear()
        self.external_urls.clear()

        # домены для определения внешних ссылок
        root_domains = {urlparse(u).netloc for u in start_urls}

        async with aiohttp.ClientSession() as session:
            # очередь: (url, depth, root_domain)
            queue: asyncio.Queue[tuple[str, int, str]] = asyncio.Queue()
            for u in start_urls:
                root_domain = urlparse(u).netloc
                await queue.put((u, 0, root_domain))

            while not queue.empty():
                url, depth, root_domain = await queue.get()

                if url in self.seen_urls:
                    continue
                self.seen_urls.add(url)

                if depth > self.max_depth:
                    continue

                html = await self.fetch(session, url)
                if not html:
                    continue

                links = self.extract_links(html, url)
                for link in links:
                    if self.is_external(link, root_domain):
                        self.external_urls.add(link)
                    else:
                        # внутренние ссылки — продолжаем обход
                        await queue.put((link, depth + 1, root_domain))

        # после обхода записываем все найденные внешние ссылки в файл
        self.save_results()

    def save_results(self) -> None:
        lines = sorted(self.external_urls)
        with open(self.output_path, "w", encoding="utf-8") as f:
            for url in lines:
                f.write(url + "\n")


async def main():
    start_urls = [
        "https://example.com",
    ]
    crawler = AsyncCrawler(max_depth=3, output_file="links.txt")
    await crawler.crawl(start_urls)
    print(f"Найдено внешних ссылок: {len(crawler.external_urls)}")
    print(f"Ссылки записаны в {crawler.output_path}")


if __name__ == "__main__":
    asyncio.run(main())