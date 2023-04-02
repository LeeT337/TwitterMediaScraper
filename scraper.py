import csv
import tkinter
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ActionChains
import tkinter as tk
import time
from datetime import datetime
import json
from lxml import etree

class Scraper:

    def __init__(self, username, password, numberTweets, account):
        self.accountToScrape = account
        self.numberTweets = numberTweets
        self.username = username
        self.password = password
        self.usernamePath = "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"
        self.passwordPath = "//div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"
        self.run = True
        self.main()


    def main(self):
        self.driver = Chrome()

        # global username
        self.driver.get("https://twitter.com/i/flow/login")

        self.sendToElement(self.usernamePath, self.username, True)
        sleep(1)
        self.sendToElement(self.passwordPath, self.password, True)
        sleep(5)

        self.scrapePage(self.accountToScrape, self.numberTweets)

        fileName = "tweetData"
        curDate = datetime.now()
        curDate = curDate.strftime("%d-%m-%Y-%H-%M-%S")
        fileName = fileName + curDate + ".csv"

        with open(fileName, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Views", "Replies", "RT's", "Likes", "Video", "Link"])
            for t in self.tweetData:
                writer.writerow([t[0], t[1], t[2], t[3], t[4], t[5], t[6]])
        return self.tweetData

        driver.quit()

    def scrapePage(self, page, numberTweets):
        self.tweetData = []
        self.scrapeHistory = []
        self.tweetPath = "//div/div/article"

        self.usernamePath = "./div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span"
        self.replyCountPath = "./div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span"
        self.retweetCountPath = "./div/div/div[2]/div[2]/div[4]/div/div[2]/div/div/div[2]/span/span/span"
        self.likeCountPath = "./div/div/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/span/span/span"
        self.viewCountPath = "./div/div/div[2]/div[2]/div[4]/div/div[4]/a/div/div[2]/span/span/span"

        self.sharePath = './/div[contains(@aria-label, "Share Tweet")]'
        self.copyLink = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div[1]/div[2]/div/span"
        self.tweetFrom = "./div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/a"

        self.videoPath = "./div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[4]/div/div[2]/div[1]/div/div/div[1]/div/div"
        print("G")
        self.driver.get(page)
        sleep(5)
        tweetsScraped = 0
        sameTweetInRow = 0
        while tweetsScraped < self.numberTweets:
            try:
                tweets = self.driver.find_elements(By.XPATH, self.tweetPath)
                #print(tweets)
                for tweet in tweets:
                    if tweet not in self.scrapeHistory:
                        print(tweetsScraped)
                        sameTweetInRow = 0
                        self.scrapeHistory.append(tweet)
                        self.scrapeHistory.append(tweet)
                        try:
                            username = tweet.find_element(By.XPATH, self.usernamePath).text
                        except:
                            username = None

                        try:
                            reply = tweet.find_element(By.XPATH, self.replyCountPath).text
                        except:
                            reply = "0"

                        try:
                            rt = tweet.find_element(By.XPATH, self.retweetCountPath).text
                        except:
                            rt = "0"

                        try:
                            like = tweet.find_element(By.XPATH, self.likeCountPath).text
                        except:
                            like = "0"

                        try:
                            view = tweet.find_element(By.XPATH, self.viewCountPath).text
                        except:
                            view = "0"

                        sleep(1)

                        self.driver.execute_script("arguments[0].scrollIntoView();", tweet)
                        sleep(1.5)

                        pathToHover = './/video[contains(@aria-label, "Embedded video")]'

                        try:
                            content = tweet.find_element(By.XPATH, pathToHover)
                        except:
                            True
                        else:
                            achains = ActionChains(self.driver)
                            achains.move_to_element(content).click().perform()
                            sleep(0.25)

                        try:
                            # checks for video timestamp bar
                            isVideo = tweet.find_element(By.XPATH, self.videoPath)
                        except:
                            isVideo = False
                        else:
                            isVideo = True

                        sleep(0.5)
                        try:
                            original = tweet.find_element(By.XPATH, self.tweetFrom).get_attribute('href')


                        except:
                            tweet.find_element(By.XPATH, self.sharePath).click()
                            sleep(1.5)
                            tweet.find_element(By.XPATH, self.copyLink).click()

                        else:
                            sharePath2 = '//div[contains(@aria-label, "Share Tweet")]'
                            showSharePath = ".//div[1]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[6]"
                            #print(original)
                            self.driver.execute_script("window.open('');")
                            self.driver.switch_to.window(self.driver.window_handles[1])
                            self.driver.get(original)
                            sleep(5)

                            page = self.driver.find_element(By.XPATH, "//body")
                            #print(page)
                            scrollTo = page.find_element(By.XPATH, showSharePath)
                            self.driver.execute_script("arguments[0].scrollIntoView();", scrollTo)
                            sleep(1.5)
                            page.find_element(By.XPATH, sharePath2).click()
                            sleep(1.5)
                            page.find_element(By.XPATH, self.copyLink).click()
                            sleep(1.5)
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])

                        link = tk.Tk().clipboard_get()

                        tweet = [username, view, reply, rt, like, isVideo, link]


                        self.tweetData.append(tweet)

                        tweetsScraped += 1
                        print(tweetsScraped)

                        #print(tweet)

                    else:
                        print(tweetsScraped)
                        print(sameTweetInRow)

                        sameTweetInRow += 1
                        if sameTweetInRow >= 25:
                            print("Break1")
                            tweetsScraped = self.numberTweets + 1
                            break

                    if tweetsScraped >= self.numberTweets or sameTweetInRow >= 25:
                        print(tweetsScraped)
                        print("Break2")
                        tweetsScraped = self.numberTweets + 1
                        break
                #print(self.tweetData)
            except:
                True

    def sendToElement(self, xpath, data, clickEnter):
        loaded = False

        while not loaded:
            try:
                element = self.driver.find_element(By.XPATH, xpath)

            except:
                sleep(3)
            else:
                loaded = True
        element.send_keys(data)
        sleep(1)
        if clickEnter:
            element.send_keys(Keys.RETURN)




