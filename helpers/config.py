import configparser, os, sys
from pathlib import Path

_DEFAULT_CONFIG = "/etc/kattis/submit/kattisrc"

_CONFIG_NOT_FOUND_MSG = """\
I failed to read in a config file from your home directory or from the
same directory as this script. Please go to your Kattis installation
to download a .kattisrc file.

The file should look something like this:
[user]
username: yourusername
token: *********

[kattis]
loginurl: https://<kattis>/login
submissionurl: https://<kattis>/submit"""


def getConfig(shouldReturnLocation = False):
    cfg = configparser.ConfigParser(converters={"array": strToArr, "command": toCommandArray})

    alternativeLocations = [
        _DEFAULT_CONFIG,
        os.path.join(str(Path.home()), ".kattisrc"),
        os.path.join(os.path.dirname(sys.argv[0]), ".kattisrc"),
    ]

    found = None
    for location in alternativeLocations:
        if os.path.exists(location):
            cfg.read(location)
            found = location

    if not found:
        print(_CONFIG_NOT_FOUND_MSG)
        if shouldReturnLocation:
            return -1, ""
        return -1

    cfg = preconfigure(cfg, found)

    if shouldReturnLocation:
        return cfg, found
    return cfg

def getUrl(cfg, option, default):
    if cfg.has_option("kattis", option):
        return cfg.get("kattis", option)
    else:
        return formatUrl(cfg.get("kattis", "hostname"), default)

def formatUrl(hostname, path):
    return "https://%s/%s" % (hostname, path)

def preconfigure(cfg, location):
    defaults = {
        "kat": {
            "language": "python",
            "openFileCommand": "",
            "workCommand": "",
        },
        "File associations": {
            ".c": "C",
            ".c#": "C#",
            ".c++": "C++",
            ".cc": "C++",
            ".cpp": "C++",
            ".cs": "C#",
            ".cxx": "C++",
            ".go": "Go",
            ".h": "C++",
            ".hs": "Haskell",
            ".java": "Java",
            ".js": "JavaScript",
            ".m": "Objective-C",
            ".pas": "Pascal",
            ".php": "PHP",
            ".pl": "Prolog",
            ".py": "Python",
            ".rb": "Ruby",
            ".fs": "F#",
            ".fsx": "F#",
            ".fsscript": "F#",
        },
        "Initialize commands": {
            "F#": "dotnet new console -lang F#",
            "C#": "dotnet new console",
        },
        "Run commands": {
            "Python": "python @f",
            "PHP": "php @f",
            "Java": "java @c",
            "C#": "dotnet run",
            "F#": "dotnet run",
            # TODO: Support rest of the languages that kattis supports
        },
        "Compile commands": {
            "Java": "javac @f"
        }
    }

    for (section, settings) in defaults.items():
        if section not in cfg.sections():
            cfg.add_section(section)
        for (key, value) in settings.items():
            _set(cfg[section], key, value)

    with open(location, "w") as configFile:
        cfg.write(configFile)
    return cfg

def _set(cfgForSection, key, value):
    if not cfgForSection.get(key, False):
        cfgForSection[key] = value

def strToArr(string):
    string = string.replace("[","").replace("]","")
    string = string.replace("'","").replace('"',"")
    return string.split(", ")

def toCommandArray(string: str):
    splitString = string.split(" ")
    return commandConvert(splitString)

def commandConvert(array: list):
    result = []
    cumulator = None
    for item in array:
        print(item, cumulator)
        if item[0] == '"' or item[0] == "'":
            cumulator = item
        elif cumulator:
            cumulator += " " + item
            if cumulator[-1] == cumulator[0]:
                result.append(cumulator)
                cumulator = None
        else:
            result.append(item)
    return result