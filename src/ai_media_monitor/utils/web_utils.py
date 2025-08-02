"""Web utilities for fetching content and bypassing paywalls."""

import asyncio

import aiohttp

from ..core.config_loader import load_config

config = load_config()


async def fetch_with_retry(
    session: aiohttp.ClientSession, url: str, retries: int = 3
) -> str | None:
    """Fetch URL with retry logic"""
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            if attempt == retries - 1:
                print(f"Failed to fetch {url}: {e}")
            await asyncio.sleep(2**attempt)  # Exponential backoff
    return None


async def bypass_paywall(session: aiohttp.ClientSession, url: str) -> str | None:
    """Try to bypass paywall using configured services"""
    for service in sorted(config.paywall_services, key=lambda x: x.priority):
        try:
            if service.url == "https://archive.ph":
                # Archive.ph requires special handling
                async with session.post(
                    f"{service.url}/submit/", data={"url": url}, allow_redirects=False
                ) as response:
                    if response.status in [302, 301]:
                        archive_url = response.headers.get("Location")
                        if archive_url:
                            return await fetch_with_retry(session, archive_url)

            elif service.url == "https://web.archive.org/save":
                # Wayback Machine
                archive_url = f"https://web.archive.org/web/{url}"
                return await fetch_with_retry(session, archive_url)

            else:
                # Generic GET services like 12ft.io, 1ft.io
                bypass_url = f"{service.url}/{url}"
                return await fetch_with_retry(session, bypass_url)

        except Exception as e:
            print(f"Paywall bypass failed with {service.url}: {e}")
            continue

    return None


async def fetch_article_content(session: aiohttp.ClientSession, url: str) -> str | None:
    """Fetch article content, using paywall bypass if needed"""
    # First try direct fetch
    content = await fetch_with_retry(session, url)

    if content and (
        "paywall" in content.lower() or "subscriber" in content.lower() or len(content) < 1000
    ):
        # Likely paywalled, try bypass
        bypassed_content = await bypass_paywall(session, url)
        if bypassed_content:
            content = bypassed_content

    return content
