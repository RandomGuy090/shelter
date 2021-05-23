# FILE = "/home/randomguy90/PROGRAM/Python/shelter/passJson.txt"
FILE = "/home/randomguy90/PROGRAM/Python/shelter/encrypted.gpg"

#used by script
PATH = ""
PATHDIR = None
GPGHOMEDIR = "/home/randomguy90/"
FIRST_READ = ""
LAST_READ = ""

#commands
EXT_KWORDS = ["q","exit","quit"]
LS_KWORDS = ["ls", "list"]
CD_KWORDS = ["", "cd"]
CD_UP_KWORDS = ["cd .."]
NEW_SHELTER_KWORDS = ["create", "mkdir", "cr","make", "new"]
NEW_FILES_KWORDS = ["add", "touch"]
DEL_KWORDS = ["del", "rm", "remove", "delete"]

#sum
COMMANDS = EXT_KWORDS + LS_KWORDS + CD_KWORDS + CD_UP_KWORDS \
		+ CD_UP_KWORDS + NEW_SHELTER_KWORDS+ NEW_FILES_KWORDS+ DEL_KWORDS