import json
from typing import Dict

import jmespath
from parsel import Selector
from playwright.sync_api import sync_playwright
from nested_lookup import nested_lookup
import json
import sys

# Note: we'll also be using parse_thread function we wrote earlier:
from scrapethread import parse_thread, scrape_thread


def parse_profile(data: Dict) -> Dict:
    """Parse Threads profile JSON dataset for the most important fields"""
    result = jmespath.search(
        """{
        profile_pic_url: .profile_pic_url,
        username: username,
        friendship_status: friendship_status,
        pk: pk,
        transparency_label: transparency_label,
        transparency_product: transparency_product,
        transparency_product_enabled: transparency_product_enabled,
        is_verified: is_verified,
        id: id,
        text_post_app_is_private: text_post_app_is_private,
        text_post_app_has_max_posts_pinned_to_profile: text_post_app_has_max_posts_pinned_to_profile,
    }""",
        data,
    )
    result["url"] = f"https://www.threads.net/@{result['username']}"
    return result



def scrape_profile(url: str) -> dict:
    """Scrape Threads profile and their recent posts from a given URL"""
    with sync_playwright() as pw:
        # start Playwright browser
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto(url)
        # wait for page to finish loading
        page.wait_for_selector("[data-pressable-container=true]")
        selector = Selector(page.content())
    parsed = {
        "user": {},
        "threads": [],
    }
    # find all hidden datasets
    hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()
    for hidden_dataset in hidden_datasets:
        # skip loading datasets that clearly don't contain threads data
        if '"ScheduledServerJS"' not in hidden_dataset:
            continue
        if 'userData' not in hidden_dataset and 'thread_items' not in hidden_dataset:
            continue
        data = json.loads(hidden_dataset)
        user_data = nested_lookup('user', data)
        thread_items = nested_lookup('thread_items', data)
        if user_data:
            parsed['user'] = user_data[0]
        if thread_items:
            threads = [
                scrape_thread(f"https://www.threads.net/@{t['post']['user']['username']}/post/{t['post']['code']}") for thread in thread_items for t in thread
            ]
            parsed['threads'].extend(threads)
    return parsed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py threads_profilename")
    else:
        profilename = sys.argv[1]
        scrap = scrape_profile("https://www.threads.net/@" + profilename)
        with open(profilename + ".json", "w") as outfile:
            json.dump(scrap, outfile, indent=4)