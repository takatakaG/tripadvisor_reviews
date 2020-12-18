import sys
import os
import time
import re
from selenium import webdriver
import pandas as pd

def get_url():    
    browser = webdriver.Chrome(executable_path="/Users/shimizutakashibun/chromedriver")
    #スタートページ
    browser.get("https://www.tripadvisor.jp/Attractions-g1021202-Activities-Tomioka_Gunma_Prefecture_Kanto.html")
    df = pd.DataFrame()
    posts=browser.find_elements_by_css_selector('div.attractions-attraction-overview-main-PoiInfo__info--260v8')
    for post in posts:
        pre1_url = post.find_element_by_css_selector('div:nth-child(1)')
        pre2_url = pre1_url.find_element_by_css_selector('div:nth-child(2)')
        url = pre2_url.find_element_by_tag_name("a").get_attribute("href")
        se = pd.Series([url], ['url'])
        df = df.append(se, ignore_index=True)
    return df

def get_details(df_url):
    details_df = pd.DataFrame()
    for i in range(len(df_url.index)): 
        print("getting info of {}".format(df_url.loc[i].url))
        browser = webdriver.Chrome(executable_path="/Users/shimizutakashibun/chromedriver")
        browser.get(df_url.loc[i].url)
        page=0

        try:

            while page < 5:
                print("######################page: {} ########################".format(page))
                print("Starting to get posts...")
                time.sleep(7)
                details_posts = browser.find_elements_by_css_selector(".ui_column.is-9")
                print(len(details_posts))
                for content in details_posts:
                    title = content.find_element_by_css_selector(".quote").text
                    comment = content.find_element_by_css_selector(".partial_entry").text
                    score_element = content.find_element_by_css_selector('div > span:first-child')
                    class_name = score_element.get_attribute('class')
                    score = int(re.search('\d+',class_name).group()) // 10

                    se = pd.Series([title,comment,score],index=['title','comment',"score"])
                    details_df = details_df.append(se, ignore_index=True)
                    print(se)
                page+=1
                browser.find_element_by_css_selector(".nav.next.taLnk.ui_button.primary").click()
                time.sleep(7)
                
            details_df.to_csv("df.csv", index=False)

        except:
            print("finished!!!!")

    return details_df

def main():
    df_url = get_url()
    review_details = get_details(df_url)

if __name__ == "__main__":
    main()