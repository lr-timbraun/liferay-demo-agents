import argparse
import asyncio
import sys
from playwright.async_api import async_playwright

async def get_dom(url, output_path):
    """
    Launches a headless browser, navigates to the URL, waits for the DOM to load,
    and saves the full rendered HTML to the specified output path.
    """
    async with async_playwright() as p:
        print(f"Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"Navigating to {url}...")
            # Wait for domcontentloaded as per the skill guide
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            print(f"Extracting DOM content...")
            content = await page.content()
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            print(f"Successfully saved DOM to: {output_path}")
            
        except Exception as e:
            print(f"Error during extraction: {e}")
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract full, rendered DOM using Playwright.")
    parser.add_argument("url", help="The URL of the page to scrape")
    parser.add_argument("--output", required=True, help="Path to the output HTML file")
    
    args = parser.parse_args()
    
    asyncio.run(get_dom(args.url, args.output))
