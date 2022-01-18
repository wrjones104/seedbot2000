"""Worlds Collide Path Examiner. Takes in a spoiler log and outputs information about possible player paths"""
from populate import populate

game = populate()
characters = game["Characters"]
dragons = game["Dragons"]
checks = game["Checks"]

for name in characters:
    print(characters[name])

for dragon in dragons:
    print(dragons[dragon])

for check in checks:
    print(checks[check])
