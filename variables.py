# FILE = "/home/randomguy90/PROGRAM/Python/shelter/passJson.txt"
FILE = ""

#used by script
PATH = ""
PATHDIR = ""
GPGHOMEDIR = "/home/randomguy90/"
FIRST_READ = ""
LAST_READ = ""
RECIP = ""
RECIP_FLAG = ""
DEL_KEYS = []
PRIV_KEY = None
PUBLIC_KEY = None
ONLINE = None
CONTENT = None
SSHPORT = 22
SSHADDR = ""

#commands
EXT_KWORDS = ["q","exit","quit"]
LS_KWORDS = ["ls", "list"]
CD_KWORDS = ["", "cd"]
CD_UP_KWORDS = ["cd .."]
NEW_SHELTER_KWORDS = ["create", "mkdir", "cr","make", "new"]
NEW_FILES_KWORDS = ["add", "touch"]
DEL_KWORDS = ["del", "rm", "remove", "delete"]
GEN_WORDS = ["gen"," generate"]

#sum
COMMANDS = EXT_KWORDS + LS_KWORDS + CD_KWORDS + CD_UP_KWORDS \
		+ CD_UP_KWORDS + NEW_SHELTER_KWORDS+ NEW_FILES_KWORDS+ DEL_KWORDS