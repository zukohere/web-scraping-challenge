def scrape():
    from splinter import Browser
    from bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd

    #Inititalize dictionary
    mars_dict = {}

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ### NASA Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)

    headline_dict={}
    teaser_dict = {}
    for page in range(0, 10):
        page = page+1
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        headlines = soup.find_all('div', class_='content_title')
        teasers = soup.find_all('div', class_='article_teaser_body')
        h_count = 1
        
        for headline in headlines:
            for teaser in teasers: 
                headline_dict[(page,h_count)]=headline.text
                teaser_dict[(page,h_count)]=teaser.text
                h_count = h_count+1

    mars_dict["news_title"] = headline_dict[(1,1)]
    mars_dict["news_p"] = teaser_dict[(1,1)]

    ### JPL Mars Space Images - Featured Image
    mars_dict["featured_image_url"] = "https://spaceimages-mars.com/image/featured/mars3.jpg"

    ### Mars Facts
    facts_url = "https://galaxyfacts-mars.com"
    tables = pd.read_html(facts_url)
    df = tables[0].merge(tables[1],how="outer")
    df = df[[0,1]]
    mars_df = df.drop([0])
    mars_df = mars_df.rename(columns={0: "Parameter", 1:"Mars Value"})
    mars_df = mars_df.reset_index(drop=True)
    html_table = mars_df.to_html()
    #Add table to dictionary
    mars_dict["html_table"] = html_table.replace('\n', '')
    mars_dict["hemisphere_image_urls"] = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg"},
        ]
    # Quit the browser
    browser.quit()

    return mars_dict

