import argparse
import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def take_screenshot(url, output_path, viewport_width=1920, viewport_height=1080):
    """
    Launches a browser, navigates to the URL, and captures a full-page screenshot.
    """
    async with async_playwright() as p:
        print(f"Launching browser for screenshot...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': viewport_width, 'height': viewport_height},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"Navigating to {url}...")
            # Wait for the network to be idle to ensure all assets/fragments are loaded
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            print(f"Capturing screenshot...")
            # Capture full page to ensure we see header/footer
            await page.screenshot(path=output_path, full_page=True)
                
            print(f"Successfully saved screenshot to: {output_path}")
            
        except Exception as e:
            print(f"Error during screenshot capture: {e}")
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture high-quality screenshots using Playwright.")
    parser.add_argument("url", help="The URL of the page to capture")
    parser.add_argument("--output", required=True, help="Path to the output image file (e.g., screenshots/homepage.png)")
    parser.add_argument("--width", type=int, default=1920, help="Viewport width (default: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="Viewport height (default: 1080)")
    
    args = parser.parse_args()
    
    asyncio.run(take_screenshot(args.url, args.output, args.width, args.height))
