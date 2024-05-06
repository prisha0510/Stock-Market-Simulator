# Stock-Market-Simulator
Simulated a stock exchange and traders interacting with it via classes in Python. The program accepts bids and offers and also defines an order matching engine which matches orders as and when they come
The major componenets of the stock market are described below:
## Stock Exchange
Stock exchange consists of the following:
1. A method that indicates the last traded price of any security
2. A method that indicates the current best bid and best offer Info on bids and asks
3. A method that indicates the top 5 bids and top 5 offers.
4. A method to accept bids or offers
5. Order Matching Engine
   1. An order matching engine matches buy and sell orders for a stock market.
   2. The Matching engine follows price-time priority for all orders
   3. When a trade is matched, the exchange collects money from the person buying the share and send it to the person selling it. The share also changes hands immediately.
   4. There is no fees for facilitating trades.
   5. The Engine only accepts orders sent during the trading hours.
   6. Any bid or offer outside of the top 5 bids or top 5 offers is cancelled and the trader is notified. Any pending orders at the end of the day are cancelled and the trader is notified.

## An Order management system (OMS) for a trader
OMS consists of the following:
1. A method to track the trader’s cash in the trading account
2. A method that indicates the current value of the trader’s portfolio
3. A method to place buy orders.
4. A method to place sell orders.

## Trader
A trader has access to the OMS. It also has an action method (An action is defined as either a buy or a sell decision on a stock)
The price at which the buy or sell order is placed should be randomized between the below three options:
1. Place order at best bid
2. Place order at best ask
3. Place order at mid-price ( mid-price = (best bid + best ask) /2 )
4. If there are no bids or offers present in the market, the trader places a buy or sell order arbitrarily 5% above or below the previous closing price. The previous close price is the price the share last traded at on the previous day.
5. If there is only a bid or only an offer on the order book, the trader chooses the opposite side at a price arbitrarily chosen amongst the best quote and 5% higher than the best bid (in case only bid is present ) and 5% lower than the best ask (in case only ask is present)

We assume that the size of the order placed (quantity) is always 1000

## Share
1. All shares of the same company are identical to each other.
2. There are no unique identifiers associated with it.

## Working of the Simulator
1. The stock exchange matching engine takes orders as they come and process them as quickly as possible while maintaining price time priority.
2. The stock exchange supports order matching on up to five stocks. Any new order that arrives will be queued in the engine.
3. An order can be placed only via the order management system (OMS). The OMS sends orders to the exchange and the Exchange notifies the OMS when an order has been fulfilled.

## Simulation
I have created 5 Trader instances with an arbitrary amount of money in their trading accounts and a random collection of stocks in their portfolio. i.e., they start with a non-zero portfolio. Assume time moves in 1 second steps. At each second, the traders arbitrarily perform a buy action or sell action. The price to buy or sell at is decided randomly as described in the prior section. If a trader runs out of money during the trading day, they stop performing buy actions. If they run out of stocks to sell, they stop performing sell actions.

An example of the output of the simulations is shown in the file log.txt
