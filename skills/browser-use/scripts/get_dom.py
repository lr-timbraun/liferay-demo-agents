import argparse
import sys
from playwright.sync_api import sync_playwright

def get_dom(url, output_path):
    print(f"Launching headless browser to scrape: {url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate and wait for DOM content to load
            print("Navigating to page and waiting for load...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Retrieve full rendered DOM HTML
            content = page.content()
            
            print(f"Saving rendered DOM to: {output_path}")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            browser.close()
            print("Scrape completed successfully!")
    except Exception as e:
        print(f"Error occurred while scraping URL {url}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Headless DOM Scraper using Playwright")
    parser.add_argument("url", type=str, help="The target URL to scrape")
    parser.add_argument("-o", "--output", type=str, required=True, help="The output file path to save the HTML DOM")
    
    args = parser.parse_args()
    get_dom(args.url, args.output)

if __name__ == "__main__":
    main()
