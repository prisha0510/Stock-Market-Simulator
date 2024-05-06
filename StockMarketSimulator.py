import random

class Stock_Exchange:

    bid_list = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[]} # stored in ascending order, price , time ,number of shares, trader is the order
    offer_list = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[]} # stored in ascending order, price , time ,number of shares, trader is the order

    def get_last_traded_price(self, stock):
        return self.last_traded[stock]
    
    def get_best_bid(self, stock): # returns best bid
        return self.bid_list[stock][-1][0]
        
    def get_best_offer(self, stock): #returns best offer
        return self.offer_list[stock][0][0]
    
    def get_top5bids(self, stock):
        return self.bid_list[stock]

    def get_top5offers(self,stock):
        return self.offer_list[stock]
        
    def add_bid(self, stock, price, time, shares, trader): # adds a bid to bid_list and maintains the bid_list as having only top 5 bids
        self.bid_list[stock].append([price, time, shares, trader])
        self.bid_list[stock].sort()
        if(len(self.bid_list[stock]) > 5):
            self.bid_list[stock] = self.bid_list[stock][:-5]

    
    def add_offer(self, stock, price, time, shares, trader): # adds an offer to offer_list and maintains the offer_list as having only top 5 offers
        self.offer_list[stock].append([price, time, shares, trader])
        self.offer_list[stock].sort()
        if(len(self.offer_list[stock]) > 5):
            self.offer_list[stock] = self.offer_list[stock][:5]
    
    def order_matching_engine(self,stock):
        n = len(self.bid_list[stock])
        m = len(self.offer_list[stock])
        
        to_delete_from_bids = [] # keeps track of bid orders that have been matched
        to_delete_from_offers = [] # keeps track of offer orders that have been matched

        for k in range(n):
            i = n-1-k
            for j in range(m):
                if i in to_delete_from_bids or j in to_delete_from_offers: # if order has already been executed, do nothing
                    continue
                
                buy_price, tm, buyer_num_shares, buyer_name = self.bid_list[stock][i]
                offer_price, tm, seller_num_shares, seller_name = self.offer_list[stock][j]
                buyer = traders[buyer_name]
                seller = traders[seller_name]

                if buyer.cash - buy_price * buyer_num_shares < 0:       #check if the order is eligible at the time of matching
                    to_delete_from_bids.append(i)
                    continue
                
                if seller.portfolio_stocks[stock] - seller_num_shares <0:       #check if the order is eligible at the time of matching
                    to_delete_from_offers.append(j)
                    continue

                if(buy_price==offer_price): # if price of a bid order and an ask order matches

                    if(buyer_num_shares == seller_num_shares): # if they have the same number of shares in their order

                        # updating cash of the traders who's orders were executed
                        
                        buyer.cash -= buy_price * buyer_num_shares
                        seller.cash += offer_price * seller_num_shares

                        # updating portfolio stocks of each trader
                        buyer.portfolio_stocks[stock] += buyer_num_shares
                        seller.portfolio_stocks[stock] -= seller_num_shares

                        # updating last traded price of the stock traded
                        last_traded[stock] = buy_price

                        # adding the executed orders from bid_list and offer_list to their respective lists
                        to_delete_from_bids.append(i)
                        to_delete_from_offers.append(j)

                    elif (buyer_num_shares > seller_num_shares):

                        # updating cash of the traders who's orders were executed

                        buyer.cash -= offer_price * seller_num_shares
                        seller.cash += offer_price * seller_num_shares

                        # updating portfolio stocks of each trader
                        buyer.portfolio_stocks[stock] += seller_num_shares 
                        seller.portfolio_stocks[stock] -= seller_num_shares

                        # updating last traded price of the stock traded
                        last_traded[stock] = offer_price

                        # adding the executed orders from bid_list and offer_list to their respective lists
                        self.bid_list[stock][i][2] -= seller_num_shares
                        to_delete_from_offers.append(j)

                    else:

                         # updating cash of the traders who's orders were executed

                        buyer.cash -= buy_price * buyer_num_shares
                        seller.cash += buy_price * buyer_num_shares

                        # updating portfolio stocks of each trader
                        buyer.portfolio_stocks[stock] += buyer_num_shares
                        seller.portfolio_stocks[stock] -= buyer_num_shares

                        # updating last traded price of the stock traded
                        last_traded[stock] = buy_price

                        # adding the executed orders from bid_list and offer_list to their respective lists
                        self.offer_list[stock][j][2] -= buyer_num_shares
                        to_delete_from_bids.append(i)
        
                buyer.cash = round(buyer.cash, 2)
                seller.cash = round(seller.cash, 2)

        to_delete_from_bids.sort()
        to_delete_from_bids.reverse()
        to_delete_from_offers.sort()
        to_delete_from_offers.reverse()

        # deleting the executed orders from offer_list
        for ind in to_delete_from_offers:
            self.offer_list[stock].pop(ind)
        
        # deleting the executed orders from bid_list
        for ind in to_delete_from_bids:
            self.bid_list[stock].pop(ind)

        
class OMS():

    def display_cash(self):
        print(self.cash)

    def display_portfolio(self):
        value = 0
        for i in 'ABCDE':
            value += self.portfolio_stocks[i]*last_traded[i]
        print(value)

    def place_buy(self, stock, shares, price): # function to place buy orders
        global clock
        global file_writer
        curr_time = display_time(clock)
        file_writer.write(self.name + " bids for " + str(shares) + " shares of stock " + str(stock) + " at " + str(price) + " Rs per share.\n")
        S.add_bid(stock, price, curr_time, shares, self.name)
        
    def place_offer(self, stock, shares, price): # function to place ask orders
        global clock
        global file_writer
        curr_time = display_time(clock)
        file_writer.write(self.name + " offers " + str(shares) + " shares of stock " + str(stock) + " at " + str(price) + " Rs per share.\n")
        S.add_offer(stock, price, curr_time, shares, self.name)

class Trader(OMS):

    def __init__(self, portfolio_stocks, cash, initial_cash, name): 
        self.portfolio_stocks = portfolio_stocks # portfolio_stocks is a dictionary, with key as the Stock and value as the number of shares of that stock
        self.cash = cash
        self.initial_cash = initial_cash
        self.name = name

    def action(self, stock):
        place_order = {"BUY": self.place_buy, "OFFER": self.place_offer}
        can_do_action = 1 # if the trader cannot do the action , this variable takes the value of 0
        bid_orders = S.bid_list[stock]
        offer_orders = S.offer_list[stock]
        my_shares = self.portfolio_stocks[stock]
        my_cash = self.cash

        if(len(bid_orders)==0 and len(offer_orders)==0): # no offers and no bids case
            
            if(my_cash == 0):
                price = 0.95 * last_traded[stock]
                buy_offer = "OFFER"
            elif (my_shares==0):
                price = 1.05 * last_traded[stock]
                buy_offer = "BUY"

            else:
                i = random.randint(0,1)
                if(i==0):
                    price = 1.05 * last_traded[stock]
                    buy_offer = "BUY"
                        
                else:
                    price = 0.95 * last_traded[stock]
                    buy_offer = "OFFER"
                   
                
        elif (len(offer_orders)==0): # no offers case

            if(my_shares==0):
                can_do_action = 0
            else:
                i = random.randint(0,1)
                if(i==0):
                    price = bid_orders[-1][0]
                else:
                    price = 1.05 * bid_orders[-1][0]
                    
                buy_offer = "OFFER"

        elif (len(bid_orders)==0): # no bids case

            if(my_cash <= 0 ):
                can_do_action = 0
            else:
                i = random.randint(0,1)
                if(i==0):
                    price = offer_orders[0][0]
                else:
                    price = 0.95 * offer_orders[0][0]

                buy_offer = "BUY"

        else:
            i = random.randint(0,2)
            j = random.randint(0,1)

            if(my_cash <= 0 and my_shares>0):
                j = 0
            elif(my_shares <= 0 and my_cash>0):
                j = 1
            elif(my_shares<=0 and my_cash<=0):
                can_do_action = 0

            if(i==0):
                price = offer_orders[0][0]   
            elif(i==1):
                price = bid_orders[-1][0]
            else:
                price = (bid_orders[-1][0]+offer_orders[0][0])/2

            buy_offer = "BUY" if j==1 else "OFFER"
               
        if(can_do_action!=0):
            existing_shares = my_shares//1000 

            if(buy_offer=='OFFER' and existing_shares > 0):
                # a trader cannot place a sell order of shares which exceed his current number of shares for that particular stock
                shares = 1000 * random.randint(1, existing_shares) 
            # if no shares, the trader cannot do the action of selling
            elif (buy_offer=='OFFER' and existing_shares == 0): 
                # since selling isn't possible, the trader does a buy action
                buy_offer = "BUY" 
                if(my_cash//(1000*last_traded[stock]) <= 0):
                     # if a buy action isn't possible because the trader doesn't have sufficient amount to buy 1000 units of that stock, the trader can neither buy nor sell, thus can_do_action is set to 0
                    can_do_action = 0
                else:
                    shares = 1000 * random.randint(1, my_cash//(1000*last_traded[stock]))
            else:
                max_buyable_shares = my_cash//(1000*last_traded[stock])
                # trader cannot place a buy order, so he places a sell order
                if(max_buyable_shares <= 0): 
                    buy_offer = "OFFER" 
                    # if the trader doesn't have shares to sell , he can do nothing
                    if(existing_shares <= 0): 
                        can_do_action = 0
                    else:
                        shares = 1000 * random.randint(1, existing_shares)
                else:
                    shares = 1000 * random.randint(1, max_buyable_shares)
            # if the trader can do some action , he/she places an order
            if(can_do_action!=0): 
                place_order[buy_offer](stock, shares, round(price,2)) 
        if can_do_action==0:
            file_writer.write(self.name + " cannot buy or sell any shares.\n")


#a function to print the contents of a dictionary
def print_dict(dict):
    global file_writer
    for k,v in dict.items():
        file_writer.write(k + ": " + str(v))
        file_writer.write('\t')

# function for displaying time from 9:00 to 15:30
def display_time(secs): 
    hrs = str(9+secs//3600)
    mins = str((secs//60)%60)
    if len(mins)==1:
        mins = '0' + mins
    sec = str(secs%60)
    if len(sec)==1:
        sec = '0' + sec
    return hrs + ":" + mins + ":" + sec
           
# this function makes the Trader 't' do an action and executes the order matching engine for that stock which the trader t took action on
def do_action_and_match(t): 
    stock_type = stock_generator[random.randint(1,5)]
    t.action(stock_type)
    S.order_matching_engine(stock_type)

#this functions simulates the stock exchange
def simulate():
    global clock
    global traders
    # 23400 is the number of seconds in 6.5 hrs
    global file_writer
    file_writer = open("log.txt", "w")
    while clock<23400:  

        file_writer.write("At " + display_time(clock) + ":\n\n")
        file_writer.write("Last Traded Price of Stocks:\n")
        print_dict(last_traded)
        file_writer.write('\n\n')
        for name,t in traders.items():
            file_writer.write(name + " cash = \t \t \t" + str(t.cash) + " Rs. \n")
            file_writer.write(name + " Portfolio = \t \t")
            print_dict(t.portfolio_stocks)
            file_writer.write('\n')
        file_writer.write('\n')

        for t in traders.values():
            do_action_and_match(t)
        clock+=1
        file_writer.write('\n')
        file_writer.write('\n')
        file_writer.write('\n')

def initialise_entities():
    global S
    global last_traded
    global traders
    global clock
    global stock_generator

    # creating 5 trader instances and one stock exchange S.
    S = Stock_Exchange()
    trader_objects = []
    trader_objects.append(Trader({'A':11000, 'B':12000, 'C':3000, 'D':20000, 'E':5000}, 40100, 40100, 'Trader 1'))
    trader_objects.append(Trader({'A':22000, 'B':6000, 'C':4000, 'D':12000, 'E':12000}, 10000, 10000, 'Trader 2'))
    trader_objects.append(Trader({'A':13000, 'B':7000, 'C':3000, 'D':15000, 'E':11000}, 5230, 5230, 'Trader 3'))
    trader_objects.append(Trader({'A':12000, 'B':5000, 'C':4000, 'D':18000, 'E':0}, 20000, 20000, 'Trader 4'))
    trader_objects.append(Trader({'A':14000, 'B':9000, 'C':14000, 'D':7000, 'E':1000}, 100, 100,'Trader 5'))

    last_traded = {'A':12, 'B':3, 'C':45, 'D':11, 'E':63}
    traders = {'Trader ' + str(i+1):trader_objects[i] for i in range(len(trader_objects))}
    clock = 0
    stock_generator = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E'}

def print_profit():
    f = open("profits.txt", "w")
    # printing the profit of each trader at the end of 6.5 hrs of trading day
    f.write("Profit of each trader at the end of the day is : \n \n")
    for t in traders.values():
        f.write("Profit of " + str(t.name) + " is " + (str(round((t.cash-t.initial_cash),2))) + " Rs.\n")
    f.close()

def print_bidlist():
    f = open("bid_list.txt", "w")
    f.write('price, time, num_shares, trader name\n')

    for ch in "ABCDE":
        f.write('Stock ' + ch + ':\n')
        st = ""
        for l in S.bid_list[ch]:
            for x in l:
                st+=str(x) + ', '
            st+='\n'
        f.write(st+'\n')
    f.close()

def print_offerlist():
    f = open("offer_list.txt", "w")
    f.write('price, time, num_shares, trader name\n')

    for ch in "ABCDE":
        f.write('Stock ' + ch + ':\n')
        st = ""
        for l in S.offer_list[ch]:
            for x in l:
                st+=str(x) + ', '
            st+='\n'
        f.write(st+'\n')
    f.close()

def close():
    print_profit()
    print_bidlist()
    print_offerlist()

    # cancelling all pending orders in the bid_list and offer_list
    for i in 'ABCDE':
        S.bid_list[i] = []
        S.offer_list[i] =[]


#main program
initialise_entities()
simulate()
close()