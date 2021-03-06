import os

from commands.web import webCommand
from enum import Enum, auto

from commands.unarchive import unarchiveCommand
from helpers.fileutils import findProblemLocation
from helpers.webutils import fetchProblem


def getCommand(problemName, options):
    message = ""
    folder = findProblemLocation(problemName)
    if folder is None:
        fetchProblem(problemName)
        message = "👍 Successfully initialized exercise", problemName + "!"
    elif folder != "":
        unarchiveCommand(problemName, [])
        message = "👍 Successfully unarchived exercise", problemName + "!"

    if message != "":
        print(message)
    if "open" in options:
        webCommand(problemName)


getFlags = [
    ("open", False),
]
