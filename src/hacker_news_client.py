import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class HackerNewsScraper:
    def __init__(self, url='https://news.ycombinator.com/', storage_dir='top_stories'):
        self.url = url
        self.storage_dir = storage_dir
        # 创建存储目录（如果不存在）
        os.makedirs(self.storage_dir, exist_ok=True)

    def fetch_and_save_stories(self):
        """Fetches the top stories from Hacker News and saves them to a file."""
        # 获取 Hacker News 页面内容
        response = requests.get(self.url)
        response.raise_for_status()  # 检查请求是否成功

        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找包含新闻的所有 <tr> 标签
        stories = soup.find_all('tr', class_='athing')

        top_stories = []
        for story in stories:
            title_tag = story.find('span', class_='titleline').find('a')
            if title_tag:
                title = title_tag.text
                link = title_tag['href']
                top_stories.append({'title': title, 'link': link})

        # 检查是否有抓取到的故事
        if not top_stories:
            print("No stories found.")
            return None

        # 获取当前日期，格式为 YYYY-MM-DD
        date_str = datetime.now().strftime('%Y-%m-%d')
        file_path = os.path.join(self.storage_dir, f'hackernews_top_stories_{date_str}.json')

        # 保存故事到文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(top_stories, file, ensure_ascii=False, indent=4)

        print(f"Top stories saved to {file_path}")
        return file_path

    def display_stories(self, stories):
        """Displays the list of stories."""
        if stories:
            for idx, story in enumerate(stories, start=1):
                print(f"{idx}. {story['title']}")
                print(f"   Link: {story['link']}")
        else:
            print("No stories found.")

if __name__ == "__main__":
    scraper = HackerNewsScraper()
    file_path = scraper.fetch_and_save_stories()
    if file_path:
        print(f"Stories have been saved to: {file_path}")
