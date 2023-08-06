# Ark-Server

## Connect
### Start Listening (connect)
Starts the server
### Receive Connect Request (accept_wrapper)
Connects to a client


## Disconnect
Disconnects the server
### Send Disconnect (send_disconnect)
Sends to a client to disconnect with the server
### Receive Disconnect (parsed from read)
If the server was remotely asked to shut down, it will then
initiate disconnecting to all remote clients too.



## Run
### Receive Connect Request
Accept the incoming connection
### Service the connection
#### Read
Read from the incoming connection
#### Write
Write to the incoming connection after reading


