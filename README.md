Make creates a docker image called 'altonomy'.
Docker-compose up starts a server using the default port 5000 on the available local ip.
The server provides 2 endpoints:
http_orderbook/<symbol in capital letters>
ws_orderbook/<symbol in capital letters>
The difference between these endpoints is that http_orderbook requests data using http api, ws_endpoint builds an orderbook using a realtime stream from a websocket.
Example urls:
http://127.0.0.1:5000/ws_orderbook/BTCUSDT
http://127.0.0.1:5000/http_orderbook/BNBBTC