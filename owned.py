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



    def sendMail(self):

        # username and password
        with open('email.txt', 'r') as f:
            self.address = f.readline()[:-1]
            self.password = f.readline()

        # create email object
        msg = MIMEMultipart()

        # define email parameters
        msg['From'] = self.address
        msg['To'] = "joelewis3335@yahoo.com"
        msg['Subject'] = "Stock update for 6/6/2018"

        # attach the body of the email
        msg.attach(MIMEText(self.msg, 'plain'))

        # open the connection to email server
        s = smtplib.SMTP(host='smtp.gmail.com', port='587')
        s.starttls()

        # login
        s.login(self.address, self.password)

        # send email
        s.send_message(msg)



    def getClose(self, ticker):
    
        # define the API URL
        url = "https://api.intrinio.com/prices?identifier=" + ticker

        # make API call
        response = requests.get(url, auth=(self.usr, self.pas))

        # convert the response to json format (dictionary)
        response = response.json()

        # return the stock close price
        return response['data'][0]['close']



    def getToday(self, ticker):

        # define the API URL
        url = "https://api.intrinio.com/prices?identifier=" + ticker

        # make API call
        response = requests.get(url, auth=(self.usr, self.pas))

        # convert the response to json format (dictionary)
        response = response.json()

        # store current and opening stock value
        current = response['data'][0]['close']
        op = response['data'][1]['close']

        # return the stock price movement for today
        return round(current-op, 2)
    



    def sendCloseEmail(self):

        # start the email message
        self.msg = "Here is your lifetime stock update:\n\n"

        # loop through the dictionary
        for name in self.own:

            # get close value
            close = self.getClose(name)

            # store buy value
            buy = float(self.own[name])

            # precent return
            val = close/buy * 100

            # check if gain or loss
            if val > 100:
                val = str(round(val-100, 2))
                tempStr = name + ' is currently up ' + val + '%\n'
            else:
                val = str(abs(round(100-val, 2)))
                tempStr = name + ' is currently down ' + val + '%\n'

            # append the new string to the message
            self.msg += tempStr

        # send the email
        self.sendMail()



    def sendTodayEmail(self):

        # start the email message
        self.msg = "Here is your daily stock update:\n\n"
        
        for name in self.own:

            # store the price movement for the day
            move = self.getToday(name)

            # check if the change is positive or negative
            if move > 0:
                val = str(move)
                tempStr = name + ' is currently up $' + val + ' today.\n'
            else:
                val = str(abs(move))
                tempStr = name + ' is currently down $' + val + ' today.\n'

            # append the new string to the message
            self.msg += tempStr

        # send the email
        self.sendMail()


if __name__ == "__main__":
    
    x = stock()

    
