# thera-py
Repo for our thera-py service which is an an NLP analyzer 


## Setup

To start the server and have it persist beyond the terminal session, use `screen`. 
From the thera-py directory, create a new `screen` with `screen -S <screen name>` 

Then run `pipenv run python index.py` and the webserver will be running. You can close the terminal window and the `screen` will still be running. 

To reconnect to the terminal where the app is running, in a new session run `screen -ls` to see active screens and `screen -r <screen name>` to reconnect. 
