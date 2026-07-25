#!/usr/bin/env python

import asyncio
import logging
import os
import json
from src.search import YoucomSearch

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def test_youcom():
    """Test You.com Search via config.json credentials."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        logger.error("config.json not found — copy config_demo.json to config.json and add your youcom.api_key")
        return

    with open(config_path) as f:
        config = json.load(f)

    youcom_key = config.get("youcom", {}).get("api_key", "")
    if not youcom_key:
        logger.error("youcom.api_key not set in config.json")
        return

    search = YoucomSearch(api_key=youcom_key, max_results=10)
    try:
        results = await search.search("Python programming", 5)
        logger.info(f"Got {len(results)} results from You.com")
        for result in results:
            logger.info(f"Title: {result.title}")
            logger.info(f"Link: {result.link}")
            logger.info(f"Snippet: {result.snippet}")
            logger.info("---")
    except Exception as e:
        logger.error(f"You.com search failed: {str(e)}", exc_info=True)


async def test_youcom_no_key():
    """Verify empty-api-key path returns no results."""
    search = YoucomSearch(api_key="", max_results=10)
    results = await search.search("test query", 5)
    assert len(results) == 0, f"Expected 0 results for empty key, got {len(results)}"
    logger.info("Empty-key path: PASS — returned 0 results")


async def main():
    logger.info("=== Test: You.com search with credentials ===")
    await test_youcom()
    logger.info("\n=== Test: You.com search with no API key ===")
    await test_youcom_no_key()


if __name__ == "__main__":
    asyncio.run(main())
