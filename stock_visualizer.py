import robin_stocks as rh
import matplotlib.pyplot as plt

tickers = []
amounts = []
prices = []
totals = []
names_dict = {}
names_list = []


def holdings():
    """Accesses the Robinhood API and returns a tuple containing my holdings"""

    login = rh.robinhood.login("", "")

    my_stocks = rh.robinhood.build_holdings() # dictionary of data
    info = my_stocks.items()

    my_holdings = { key : value['quantity'] for key, value in info } # creates a dictionary containing my holdings

    for ticker in my_holdings.keys():
        tickers.append(ticker)
    for quantity in my_holdings.values():
        amounts.append(float(quantity))

    print("")
    print("My Holdings:", my_holdings)
    print("")

def current_price():
    """turns prices into a list of the current prices"""
    
    str_prices = rh.robinhood.get_latest_price(tickers[0:]) # creates a list of strings representing stock prices
    float_prices = list(map(float, str_prices)) # converts the list of strings into a list of floats

    
    prices.extend(float_prices)
    

def calculate_totals():
    """turns totals into a list containing the equity for each stocks"""
    for index in range(0, len(amounts)):
        total_price = prices[index] * amounts[index]
        total_price = round(total_price, ndigits=2)
        totals.append(total_price)

    

def construct_lists():
    """constucts the lists needed for pichart"""
    holdings()
    current_price()
    calculate_totals()

    print("Tickers:", tickers)
    print("Amounts:", amounts)
    print("Prices:", prices)
    print("Totals:", totals)
    print("")

def construct_names_dict():
    """creates a dictionary with symbols as keys and names as values"""
    names = rh.robinhood.get_instruments_by_symbols(tickers[0:-1], info='simple_name')
    for i, name in enumerate(names):
        names_dict[tickers[i]] = name
    print(names_dict)

construct_lists()
construct_names_dict()
print("")
portfolio_value = round(sum(totals), ndigits=2)
print(portfolio_value)


for key in names_dict:
    name_string = key + " - " + names_dict[key]
    names_list.append(name_string)
names_string = " | ".join(names_list)

fig, ax = plt.subplots(figsize=(16,8))
ax.set_facecolor('#FAEAC6')
ax.figure.set_facecolor('#FAEAC6')
ax.tick_params(axis='x', colors='#38302E')
ax.tick_params(axis='y', colors='#38302E')

ax.set_title("My Portfolio Visualizer", color='#38302E', fontsize=20)

patches, texts, autotexts = ax.pie(totals, labels=tickers, autopct='%1.1f%%', pctdistance=0.8)
[text.set_color('#38302E') for text in texts]

my_circle = plt.Circle((0,0), 0.55, color='#FAEAC6')
plt.gca().add_artist(my_circle)

ax.text(-2, 0.95, 'Portfolio Overview', fontsize=12, color='#38302E', verticalalignment='center', horizontalalignment='center')
ax.text(0, -1.25, 'Portfolio Value: ${}'.format(portfolio_value), fontsize=17, color='#38302E', verticalalignment='center', horizontalalignment='center')
ax.text(0, -1.40, '[{}]'.format(names_string), fontsize=8, color='#38302E', verticalalignment='center', horizontalalignment='center')
counter = 0.15
for i, ticker in enumerate(tickers):
    ax.text(-2, 0.95 - counter, '{} : ${}'.format(ticker, totals[i]), fontsize=10, color='#38302E', verticalalignment='center', horizontalalignment='center')
    counter += 0.15
                                   


plt.show()
   
    


    
    

