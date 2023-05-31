import csv
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def main():

    base_url = 'https://news.ycombinator.com/item?id=22665398'
    keywords = {
        "python": 0,
        'javascript': 0,
        'rust': 0,
        'typescript': 0,
        'ruby': 0,
        'java': 0,
        'c#': 0
    }

    for page in range(1, 6):
        url = f'{base_url}&p={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        elements = soup.find_all(class_='ind', indent=0)
        comments = [e.find_next(class_='comment') for e in elements]

        for comment in comments:
            comment_text = comment.get_text().lower()
            words = comment_text.split(' ')
            words = {w.strip('.,!@/:;') for w in words}

            for k in keywords:
                if k in words:
                    keywords[k] += 1

    print(keywords)

    plt.bar(keywords.keys(), keywords.values())
    plt.xlabel("Language")
    plt.ylabel('#Number of posts')
    plt.show()


if __name__ == '__main__':
    main()
