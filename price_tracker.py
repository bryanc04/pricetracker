import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.linear_model import LinearRegression


#Function to downlaod file based on stock_symbol in csv format
def download_file(stock_symbol):
    yahoo_finance_url = f"https://finance.yahoo.com/quote/{stock_symbol}/history/"


    # get the current working directory
    current_dir = os.getcwd()

    # set downlaod path to cwd
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": current_dir}
    chrome_options.add_experimental_option('prefs', prefs)


    # create the Chrome webdriver with the specified options
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # open yahoo finance
    driver.get(yahoo_finance_url)

    # wait
    time.sleep(3)

    close_button = driver.find_element(By.XPATH, "//*[@id='myLightboxContainer']/section/button[1]")
    close_button.click()

    time.sleep(3)

    download_file = driver.find_element(By.XPATH, "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[1]/div[2]/span[2]/a")
    download_file.click()

    time.sleep(10)

    # close 
    driver.quit()

#get stock symbol as input, input validation would be very tedios so not done
stock_symbol = input("Enter a valid stock symbol, this code will not work for invalid symbols: ")

#check if csv is already downlaoded, download if not
if not (os.path.exists(f"{stock_symbol}.csv")):
    download_file(stock_symbol)

#read in csv
df = pd.read_csv(f"{stock_symbol}.csv")

fig, axs = plt.subplots(1,2)

#read x and y values
x = df["Date"]
y = df["Close"]

#x and y for prediction purposes
X = np.arange(len(df)).reshape(-1, 1)
Y = df["Close"].values

lr_model = LinearRegression()
lr_model.fit(X, Y)

#get necessary values for prediction
slope = lr_model.coef_[0]
intercept = lr_model.intercept_

future_dates = pd.date_range(start="2023-04-01", end="2024-04-01", freq="M")


xticks = [ i for i in range(0, len(df["Date"]), 10) ]
xticklabels = [ df["Date"][i][2:] for i in range(0, len(df["Date"]), 10)]


axs[0].plot(x, y)
axs[0].set_xticks(xticks)
axs[0].set_xticklabels(xticklabels, rotation=90)

# Set plot title and axis labels
axs[0].set_title(f"{stock_symbol} chart")
axs[0].set_xlabel("Date")
axs[0].set_ylabel("Closing price($USD)")

#plot the predicted line based on slope and intercept
axs[1].plot(future_dates, slope * np.arange(len(future_dates)) + intercept, label="Linear Regression")

axs[1].set_title("A bit stupid linear regression based on general trend, it doesn't actually work")
axs[1].set_xlabel("Date")
axs[1].set_ylabel("Closing price($USD), but a bit off")


plt.show()


