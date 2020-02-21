
### Mini project: Websocket game

Create a server and client implementation of a follow-me like game. It doesn't need to have a web UI with it.
Simple terminal based servers would suffice.

+ When a key is pressed in server (instruction), the client receives it; 
and has a timer counting up to X seconds in which the same key has to be 
pressed. 

+ The server verifies if the keypress sent by client matched “the 
instruction” and assign +1 point on correct, -1 on a wrong key and 0 for 
timeouts. 

+ The game is over when the score reaches either +10 points or -3 points. 

+ The game is also over if the client does not respond for 3 continuous 
instructions. 

- Each score update should send the score back to the connected client. 

- The client should also know the timeout value for each instruction 
received.
