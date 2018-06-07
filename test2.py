# used in API call
from requests.auth import HTTPBasicAuth
import requests

# used to read in stock data
from csv import reader

# used to send email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class stock:

    def __init__(self):

        self.msg = "Here is your stock update:\n\n"

        # define dictionary to hold stocks
        self.own = {}

        # read the username and pass from text file
        with open('logIn.txt', 'r') as f:
            self.usr = f.readline()[:-1]
            self.pas = f.readline()

        # read in current stock info
        with open('own.csv', 'r') as csvfile:

            # converts contents to list form
            contents = reader(csvfile)

            # skip the header
            next(contents)

            # store buy price with the stock ticker
            for row in contents:
                self.own[row[0]] = row[1]



    def getClose(self, ticker):
    
        # define the API URL
        url = "https://api.intrinio.com/prices?identifier=" + ticker

        # make API call
        response = requests.get(url, auth=(self.usr, self.pas))

        # convert the response to json format (dictionary)
        response = response.json()

        # return the stock close price
        return response['data'][0]['close']
    



    def collectClose(self):

        # define list to hold close values
        self.close = []

        # loop through the dictionary
        for name in self.own:

            # get close value
            close = self.getClose(name)

            # get buy value
            buy = float(self.own[name])

            # precent return
            val = close/buy * 100

            # check if gain or loss
            if val > 100:
                val = str(round(val-100, 2))
                tempStr = name + ' is currently up %' + val + '\n'
            else:
                val = str(abs(round(100-val, 2)))
                tempStr = name + ' is currently down %' + val + '\n'

            self.msg += tempStr



    def sendMail(self):

        a = "JoeLewis3335@gmail.com"
        p = "Laxlife123"

        msg = MIMEMultipart()

        msg['From'] = a
        msg['To'] = "joelewis3335@yahoo.com"
        msg['Subject'] = "Stock update for 6/6/2018"

        msg.attach(MIMEText(self.msg, 'plain'))

        s = smtplib.SMTP(host='smtp.gmail.com', port='587')
        s.starttls()
        s.login(a, p)

        s.send_message(msg)



if __name__ == "__main__":
    
    x = stock()
    x.collectClose()
    x.sendMail()

    
