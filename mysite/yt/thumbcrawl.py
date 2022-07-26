from bs4 import BeautifulSoup
from selenium import webdriver

thumb_info = {
    'thumb_link': ''
}


def get_thumb_link(target_url):
    path = 'C://Users//Jaemin Lee//Desktop//가상환경//chromedriver'
    driver = webdriver.Chrome(path)

    delay = 3
    driver.implicitly_wait(delay)
    driver.get(target_url)

    body = driver.find_element_by_tag_name('body')

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    lis = soup.find_all('div', id="channel-header-container")
    thumb_link = lis[0].find('img', {'src': True})['src']
    global thumb_info
    thumb_info = {
        'thumb_link': thumb_link
    }
    return thumb_info


if __name__ == '__main__':
    print('hi')