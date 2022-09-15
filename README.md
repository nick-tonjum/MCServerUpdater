# MCServerUpdater
A tool that keeps your Minecraft server up to date.


# Installation

  - Install requirements using `pip3 install -r requirements.txt`
  - Make a new folder in your Minecraft Server folder and put these files (MCServerUpdater.py and config.txt) inside it. 
  - Enable RCON for your Minecraft Server and set a password for it (I highly recommend NOT using your personal password)
  - Enter your RCON information in the MCServerUpdater config.txt

  
# Usage

  - Change your preferred server and release type in config.txt
  - Launch tool with `python3 MCServerUpdater.py`

# Configuration

  -`serverjarname = server.jar` -> The file name of your server JAR. This should ALWAYS end with '.jar'
  -`servertype = Paper` -> The type of server you're running. Paper is currently the only supported version.
  -`rconport = 25575` -> RCON Port to your server. This is configurable in your server.properties
  -`rconpassword = secret` -> RCON Password to your server from your server.properties. DO NOT USE A PERSONAL PASSWORD!
  -`updateinterval = 3600` -> The amount of time in seconds the tool will check for an update.
  -`notificationmessage = {"text":"Server restarting in 10 seconds...","color":"yellow"}` -> The JSON format message the server will display when shutting down
  -`shutdowndelay = 10` -> The amount of time in seconds it will take after the notification for the server to shut down.
  -`shutdowncommand = stop` -> The command to execute for shutting down the server 
  -`serverstartscript = start.sh` -> The server start script to call after updating process is complete (.bat or .sh)
