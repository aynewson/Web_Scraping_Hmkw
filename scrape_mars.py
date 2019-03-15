from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

#URLs
mars_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

mars_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

twitter_news = 'https://twitter.com/marswxreport?lang=en'

mars_hemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

mars_facts = "https://space-facts.com/mars/"


#Chrome Driver
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


#Intialize the browser
#Mars News
browser = init_browser()
def scrape_marsDetails():
    browser.visit(mars_news)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    newsDetails = soup.findAll('ul', attrs={'class': 'item_list'})
    counter = 0;    

    for articlesList in newsDetails:
        for indArticle in articlesList:
            if counter == 0:
                news_date = indArticle.find('div', attrs={'class': 'list_date'}).text
                news_title = indArticle.find('div', attrs={'class': 'content_title'}).text
                news_para = indArticle.find('div', attrs={'class': 'article_teaser_body'}).text
                counter = counter + 1

#Mars Image
    browser.visit(mars_image)
    html = browser.html 
    soup = BeautifulSoup(html, 'lxml')

    featuredImage = soup.find('article', attrs={'class':'carousel_item'})
    featuredImageBuffer = featuredImage.attrs['style']
    featured_image_url = "https://www.jpl.nasa.gov" + featuredImageBuffer[featuredImageBuffer.find('url') + 5: len(featuredImageBuffer) - 3]

#Twitter
    counter = 0 
    browser.visit(twitter_news)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    allTweets = soup.find_all('div', attrs={'class': 'js-tweet-text-container'})

    for a in allTweets:
        if("Sol" in a.find('p').text and "pressure" in a.find('p').text and "daylight" in a.find('p').text and counter == 0):

            mars_weather = a.find('p').text

            counter = counter + 1

#Mars Hemisphere
    browser.visit(mars_hemisphere)
    html = browser.html 
    soup = BeautifulSoup(html, 'lxml')

    marshemisphere = soup.findAll('div', attrs={'class': 'item'})
    image_list = []
    for a in marshemisphere: 
        for b in a.findAll('a'):
            if(len(b.text) > 0):
                image_list.append(b.text)

#Mars Facts
    browser.visit(mars_facts)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    tables = pd.read_html(mars_facts)
    df = tables [0]
    df.columns = ['desc', 'facts']
    desc = df['desc'].values.tolist()
    facts = df['facts'].values.tolist()

#Creating Dictionaries 
    hemisphere_images = []
    title_list = []
    image_list = []

    for text in image_list:
        browser.visit(mars_hemisphere)
        html = browser.html

        browser.click_link_by_partial_text(text)

        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        image = soup.find_all('img')
        for a in image:
            if('full' in a.get('src')):
                dictDetails = {'title':text, 'img_url' : 'https://astrogeology.usgs.gov' + a.get('src') }
                title_list.append(text)

                image_list.append('https://astrogeology.usgs.gov' + a.get('src') )

                hemisphere_images.append(dictDetails)

    marsDetails = {
        'news_para' : news_para, 
        "news_title": news_title,
        "featured_image_url": featured_image_url,
        "marshemisphere": marshemisphere,
        "desc":desc,
        "facts":facts,
        "titleList": titleList,

            "imageList":imageList,

            "hemisphere_image_urls":hemisphere_image_urls
            
        }
    return marsDetails      