from websocket import create_connection

ws = create_connection("ws://localhost:9909/ws")
print "Sending 'Hello, World!' ..."
ws.send("fresh")
print "Sent"
print "Reciving ..."
result = ws.recv()
print "Recived '%s'" % result
ws.close()
