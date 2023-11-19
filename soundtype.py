import json
import re

with open('SampleTypes.json') as f:
    SampleTypes = json.load(f)

class soundtype:
    def __init__(self, name, path, logger) -> None:
        self.name = name
        self.path = path
        self.logger = logger
        self.logger.info(f"Analyzing {self.path}")
        self.checktype()

    def checktype(self):
        for instr in SampleTypes:  # Loop through Json file
            for typess in instr['types']:
                if re.search(typess, self.name, re.IGNORECASE):  # Regex expression search for match
                    self.type = typess
                    self.sorting = f"{instr['instr']}\\{typess}"
                    return True
                else:  # If no match, then unclassified
                    self.type = "Unclassified"
                    self.sorting = "Unclassified"
