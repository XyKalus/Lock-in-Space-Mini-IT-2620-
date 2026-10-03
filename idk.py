import pathlib
from pathlib import Path

events = Path.cwd()/"events"
print(events)

for file in events.iterdir():
    print(file.name)