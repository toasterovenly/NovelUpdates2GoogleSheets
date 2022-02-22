import collections
import argparse
from datetime import datetime
import json
import re
from settings import load as settingsLoad

################################################################################

outPath = "output\\"
settings = {} # from settings file
options = {} # from command line

################################################################################

def foo(gameData):
	return

################################################################################
# handle command line args

def parse():
    parser = argparse.ArgumentParser(description="Get your boardgame collection"
                                     + " from Board Game Geek.")
    parser.add_argument("userName",
                        help="The username of the player whose collection you want.")
    # parser.add_argument("-f", "--force", action='store_true',
    #                     help="Force retrieve the user's full collection from bgg.com,"
    #                     + " otherwise only updates will be retrieved. You'll need to do"
    #                     + " this if you delete items from your collection.")
    parser.add_argument("-i", "--intermediate", action='store_true',
                        help="Output intermediate xml files. This is useful if you want"
                        + " to create homerules.")
    parser.add_argument("-p", "--player-name", dest="playerName",
                        help="The name of the human player that this user represents.")
    parser.add_argument("-r", "--retries", type=int, default=5,
                        help="Number of times to request info from BGG before giving up.")
    parser.add_argument("-s", "--settings-file", dest="settingsFile", default="settings.json",
                        help="Path to a settings file to load. Default is 'settings.json'.")
    parser.add_argument("-t", "--timestamp", action='store_true',
                        help="Output files will have a timestamp appended to their name.")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Print verbose output.")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.1')

    args = parser.parse_args()
    args.time = datetime.now()
    if args.timestamp:
        args.filePostfix = args.time.strftime("-%Y%m%d%H%M%S")
    else:
        args.filePostfix = ""
    args.outFile = outPath + args.userName + args.filePostfix + ".pdf"
    args.outPath = outPath

    print("get collection for user '" + args.userName + "'.")
    if args.verbose:
        print("got args", args)
    return args

def parseSettings(args):
    with open(args.settingsFile) as file:
        data = json.load(file)
        print("json", type(data), data)
    return data

################################################################################

options = parse()
settings = settingsLoad(options.settingsFile)
settings["options"] = options
# purposefully import these after settings are loaded
import netCode
import pdfWriter
process(options)
print("done.")
