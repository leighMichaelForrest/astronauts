from pathlib import Path
from random import choice
import json
import wikipedia
import requests


def format_name(name, in_name=True):
    """Format a name for wikipedia module. in_name is True if validating a name
    for the data store. False if retrieving data."""
    if in_name:
        return name.replace('kiy', 'ky').replace(' ', '_').lower()
            # richard_arnold throws DisambiguationError, so change it
    else:
        return name.replace('_', ' ').title()


class AstronautDictionary:
    def __init__(self, data_file):
        self.data_file = Path(data_file)
        if self.data_file.exists():
            # Read file
            self._get()
        else:
            # make dictionary
            self.astro_dict = {}
            # make file and save dictionary to file
            self._save()

    def _get(self):
        """Get dictionary from json"""
        with self.data_file.open() as f:
            # save json to internal dictionary
            self.astro_dict = json.load(f)

    def _save(self):
        """Save the current dictionary to json file"""
        # w+ flag adds file if not in directory
        with self.data_file.open('w+') as f:
            json.dump(self.astro_dict, f)

    def get_astronaut(self, astronaut):
        """"""
        astronaut = format_name(astronaut)
        
        # richard_arnold throws DisambiguationError, so change it
        if astronaut == 'richard_arnold':
            astronaut = 'richard_r_arnold'

        if astronaut in self.astro_dict:
            return self.astro_dict[astronaut]
        else:
            try:
                astro_data = {}
                astro = wikipedia.page(astronaut)
                print(astro)
                astro_data['display_name'] = format_name(astronaut, False)
                astro_data['url'] = astro.url
                astro_data['summary'] = astro.summary
                # TODO: get official image
                # add it to the dictionary
                self.astro_dict[astronaut] = astro_data
                # save dictionary
                self._save()
            except wikipedia.exceptions.PageError:
                print("PAGE ERROR")
            except wikipedia.exceptions.DisambiguationError:
                print("DISAMBIGUATION ERROR")
            finally:
                return self.astro_dict[astronaut]

    def get_astronauts(self):
        astronaut_data = []
        astronauts = requests.get('http://api.open-notify.org/astros.json').json()
        # fetch the data
        for astronaut in astronauts['people']:
            astronaut_data.append(self.get_astronaut(astronaut['name']))
        return astronaut_data


if __name__ == '__main__':
   pass
