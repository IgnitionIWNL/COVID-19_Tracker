from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import requests
import threading

counts = []
# icon = pystray.Icon('COVID-19 Tracker')
# # Generate an image
# image = Image.new('RGB', (25, 25))
# dc = ImageDraw.Draw(image)
# dc.rectangle((25 // 2, 0, 25, 25 // 2))
# dc.rectangle((0, 25 // 2, 25 // 2, 25))

# icon.icon = image

URL = 'https://www.worldometers.info/coronavirus/country/us/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'lxml')

tables = soup.find_all('table')[1];
table_rows = tables.find_all('tr')

def main():
    print('Starting scheduler...')
    # icon.run(setup)
    scheduler()

# def setup(icon):
#     icon.visible = True;

def notify(state, oldCount, newCount):
    toaster = ToastNotifier()
    toaster.show_toast("New COVID-19 Cases Reported in {}!".format(state), "Previous case count was {}. New case count is {}.".format(oldCount, newCount), duration=5, threaded=True)

def scheduler():
    getData()
    threading.Timer(60.0, scheduler).start()

def getData():
    for tr in table_rows:
        td = tr.find_all('td')
        if len(td) < 4:
            continue
        row = [i.text for i in td]
        
        if 'Michigan' in row[0]:
            #print('State: {} | Current Count: {} | Change: {}'.format(row[0].strip(), row[1].strip(), row[2].strip()))
            ####COUNTS IS [OLD COUNT, NEW COUNT]####
            if counts == []:
                print("Counts is less than 1...must be first run")
                counts.append(row[1].strip())
                #print(counts)
            elif len(counts) == 1:
                counts.append(row[1].strip())
                #counts.append('2,000')
                if counts[0] != counts[1]:
                    print("New COVID-19 cases in {}! Old count was {}, new count is {}".format(row[0].strip(), counts[0], counts[1]))
                    notify(row[0].strip(), counts[0], counts[1])
            elif len(counts) == 2:
                #print('Old Count: {} | New Count: {}'.format(counts[0], counts[1]))
                counts[0] = counts[1]
                counts.pop(1)
                counts.append(row[1].strip())

                #check that OLD != NEW and NEW > OLD
                if counts[0] != counts[1] and counts[1] > counts[0]:
                    print("New COVID-19 cases in {}! Old count was {}, new count is {}".format(row[0].strip(), counts[0], counts[1]))
                    #toaster.show_toast("New COVID-19 Cases reported in ", "Previous case count was . New case count is ", duration=10, threaded=False)
                    notify(row[0].strip(), counts[0], counts[1])
                else:
                    print("No new cases of COVID-19 reported in {}".format(row[0].strip()))

main()