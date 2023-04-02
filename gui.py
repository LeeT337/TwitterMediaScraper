import tkinter as tk
from scraper import Scraper


class Gui:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Twitter media scraper")
        self.root.geometry("1400x600")

        self.usernameFrame = tk.Frame(self.root, width=100)
        self.usernameFrame.columnconfigure(0, weight=1)
        self.usernameFrame.grid(row=0, column=0)
        self.passwordFrame = tk.Frame(self.root, width=100)
        self.passwordFrame.columnconfigure(0, weight=1)
        self.passwordFrame.grid(row=1, column=0)
        self.accountFrame = tk.Frame(self.root, width=100)
        self.accountFrame.columnconfigure(0, weight=1)
        self.accountFrame.grid(row=2, column=0)
        self.tweetFrame = tk.Frame(self.root, width=100)
        self.tweetFrame.columnconfigure(0, weight=1)
        self.tweetFrame.grid(row=3, column=0)

        self.usernameLabel = tk.Label(self.usernameFrame, text="Username:")
        self.usernameLabel.grid(row=0, column=0)
        self.usernameEntry = tk.Entry(self.usernameFrame)
        self.usernameEntry.grid(row=0, column=1)

        self.passwordLabel = tk.Label(self.passwordFrame, text="Password:")
        self.passwordLabel.grid(row=0, column=0)
        self.passwordEntry = tk.Entry(self.passwordFrame)
        self.passwordEntry.grid(row=0, column=1)

        self.accountLabel = tk.Label(self.accountFrame, text="Account to scrape:")
        self.accountLabel.grid(row=0, column=0)
        self.accountEntry = tk.Entry(self.accountFrame)
        self.accountEntry.grid(row=0, column=1)

        self.tweetLabel = tk.Label(self.tweetFrame, text="Number of tweets to scrape:")
        self.tweetLabel.grid(row=0, column=0)
        self.tweetEntry = tk.Entry(self.tweetFrame)
        self.tweetEntry.grid(row=0, column=1)



        self.startButton = tk.Button(self.root, text="Start scraping", command=self.main)
        self.startButton.grid(row=5, columns=1)

        self.root.mainloop()

    def main(self):
        setupData = self.getSetupData()
        tweetData = Scraper(setupData[0], setupData[1], setupData[2], setupData[3])


    def getSetupData(self):


        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        self.account = self.accountEntry.get()
        self.accountToScrape = "https://twitter.com/" + self.account + "/media"
        self.numberTweets = self.tweetEntry.get()
        return [self.username, self.password, int(self.numberTweets), self.accountToScrape]