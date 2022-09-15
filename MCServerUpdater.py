import os
import tkinter
import requests
import ast
import configparser
from mcrcon import MCRcon
from time import sleep
import shutil



## Load configuration
config = configparser.ConfigParser()

if os.path.exists("config.txt"):
    config.read("config.txt")
else:
    print("Generating new config file...")
    config["MCServerUpdater"] = {'serverjarname': 'server.jar', 'servertype': 'Paper', 'RconPort': 25575, 'RconPassword': 'secret','UpdateInterval': 3600,'NotificationMessage': '{"text":"Server restarting in 10 seconds...","color":"yellow"}','ShutdownDelay': 10,'ShutdownCommand': 'stop','ServerStartScript': 'None'}
    with open("config.txt","w") as conf:
        config.write(conf)
    config.read("config.txt")

## Test RCON connectivity

try:
    with MCRcon("127.0.0.1",config["MCServerUpdater"]["rconpassword"],int(config["MCServerUpdater"]["rconport"])) as mcr:
        resp = mcr.command("/help")
except Exception as e:
    print("Could not connect to RCON. Is it enabled in your server configuration? Is the password correct?")


## Update checking procedure for Paper

def Update_Paper():
    print("Checking for update...")
    with MCRcon("127.0.0.1",config["MCServerUpdater"]["rconpassword"],int(config["MCServerUpdater"]["rconport"])) as mcr:
        resp = mcr.command("icanhasbukkit")
        sleep(2)
        if "Paper-" not in resp:
            print("Waiting on server...")
            sleep(5)
            resp = mcr.command("icanhasbukkit")
        splitresponse = resp.split(" ")
        for piece in splitresponse:
            if "Paper-" in str(piece):
                currentpaperversion = str(splitresponse[int(splitresponse.index(piece)) + 2])[:-1] + "-" + str(piece)[10:]
    print("Current Paper Version: " + currentpaperversion)
        
    response = requests.get("https://papermc.io/api/v2/projects/paper/")
    versiondict = ast.literal_eval(response.text)
    latestversion = versiondict["versions"][-1]
    response = requests.get("https://papermc.io/api/v2/projects/paper/versions/" + latestversion)
    builddict = ast.literal_eval(response.text)
    latestbuild = builddict["builds"][-1]
    latestserverversion = str(latestversion)+ "-" + str(latestbuild)
    print("Latest Paper Release: " + latestserverversion)

    if not int(currentpaperversion.replace(".","").replace('-',"")) >= int(latestserverversion.replace(".","").replace('-',"")):
        print("Server is up to date.")
    else:
        print("Downloading new update...")
        url = str("https://api.papermc.io/v2/projects/paper/versions/" + latestversion + "/builds/" + str(latestbuild) + "/downloads/paper-" + latestversion + "-" + str(latestbuild) + ".jar")
        with requests.get(url, stream=True) as r:
            with open(str(config["MCServerUpdater"]["serverjarname"]), 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print("Done.")
        
        ## Shutdown Server

        with MCRcon("127.0.0.1",config["MCServerUpdater"]["rconpassword"],int(config["MCServerUpdater"]["rconport"])) as mcr:
            mcr.command("tellraw @a " + config["MCServerUpdater"]["notificationmessage"])
            sleep(int(config["MCServerUpdater"]["shutdowndelay"]))
            mcr.command(str(config["MCServerUpdater"]["shutdowncommand"]))

        ## Replace Server Jar with new one (try every second until success or 50 fails)



Update_Paper()