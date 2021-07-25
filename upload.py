from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import random
import os

if not os.path.exists('./otherComments'):
    os.mkdir('./otherComments')
path = r"C:\Users\hank\Desktop\upload"

browser = webdriver.Chrome(path)
url='https://www.tripadvisor.com.tw/Restaurants-g293913-Taipei.html'
for i in range(1):
    browser.get(url)
    res=browser.page_source
    soup=BeautifulSoup(res, 'html.parser')

    for restTags in soup.select('a[class="_15_ydu6b"]'):
        try:
            restUrl='https://www.tripadvisor.com.tw'+restTags['href']            
            k=1
            while k!=0:
                try:
                    browser.get(restUrl)
                    restRes=browser.page_source
                    restSoup=BeautifulSoup(restRes, 'html.parser')
                    restName=restSoup.select('h1[class="_3a1XQ88S"]')[0].text
                    for commentList in restSoup.select('div[class="rev_wrap ui_columns is-multiline"]'):
                        commenter=commentList.select('div[class="info_text pointer_cursor"]')[0].text
                        commentNum=commentList.select('span[class="badgeText"]')[0].text
                        if commentNum!="1則評論":
                            print('*****'+commenter)
                            commenterUrl='https://www.tripadvisor.com.tw/Profile/'+commenter
                            browser.get(commenterUrl)
                            commenterRes=browser.page_source
                            commenterSoup=BeautifulSoup(commenterRes, 'html.parser')
                            for otherCommentList in commenterSoup.select('div[class="nMewIgXP ui_card section"]'):
                                otherRestName=otherCommentList.select('div[class="_2ys8zX0p ui_link"]')[0].text
                                if otherRestName!=restName:
                                    commentType=otherCommentList.select('div[class="_7JBZK6_8 _20BneOSW"] span')[0]['class'][1]
                                    otherRestLocation=otherCommentList.select('div[class="_7JBZK6_8 _20BneOSW"]')[0].text
                                    otherRestRating=otherCommentList.select('div[class="_1VhUEi8g _2K4zZcBv"] span')[0]['class'][1].split('bubble_')[-1]
                                    otherCommTitle=otherCommentList.select('div[class="_3IEJ3tAK _2K4zZcBv"]')[0].text
                                    otherComment=otherCommentList.select('div[class="_133ThCYf"] q')[0].text
                                    otherRestUrl='https://www.tripadvisor.com.tw'+otherCommentList.select('div[class="_2X5tM2jP _2RdXRsdL _1gafur1D"] div a')[0]['href']
                                    with open('./otherComments/{}.txt'.format(restName), 'a', encoding='utf-8') as f:
                                        f.write('評論帳號: '+commenter+'\n')
                                        f.write('評論種類: '+commentType+'\n')
                                        f.write('餐廳名稱: '+otherRestName+'\n')
                                        f.write('餐廳位置: '+otherRestLocation+'\n')
                                        f.write('評論分數: '+str(int(otherRestRating)/10)+'\n')
                                        f.write('評論標題: '+otherCommTitle+'\n')
                                        f.write('評論內容: '+otherComment+'\n')
                                        f.write('餐廳連結: '+otherRestUrl+'\n')
                                        f.write('------'+'\n')

                                else:
                                    pass
                            time.sleep(random.randint(3, 5))
                        else:
                            pass
                    newRestUrl='https://www.tripadvisor.com.tw'+restSoup.select('a[class="nav next ui_button primary"]')[0]['href']
                    restUrl=newRestUrl
                    print('***Click 手動載入，' + restName + '留言第' + str(k+1) + '頁***')    
                    k=k+1
                    time.sleep(random.randint(4, 6))
                except:
                    k=0
                    print(restName + 'has no more comments')                        
        except IndexError:
            print(IndexError)
            break
        time.sleep(random.randint(1, 5))
        
    newUrl = 'https://www.tripadvisor.com'+soup.select('a[class="nav next rndBtn ui_button primary taLnk"]')[0]['href']
    url=newUrl



driver.close()
driver.quit()