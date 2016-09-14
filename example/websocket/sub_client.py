from websocket import create_connection
import time

ws = create_connection("ws://localhost:9909/ws")
print "Sending 'Hello, World!' ..."
ws.send("Hey, I am new user")
print "Sent"
counter = 0
while True:
	counter+=1
	print "Reciving ..."
	result = ws.recv()
	print "[%d]Recived '%s'" % (counter,result)
ws.close()
