from pathlib import Path
import json
import wikipedia
import requests


def format_name(name, in_name=True):
    """Format a name for wikipedia module. in_name is True if validating a name
    for the data store. False if retrieving data."""
    if in_name:
        return name.replace('kiy', 'ky').replace(' ', '_').lower()
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

    def set_data(self, astronaut):
        """"""
        # format the name
        astronaut = format_name(astronaut)

        if astronaut not in self.astro_dict:
            try:
                # if entry does not exist, get the data
                astro = wikipedia.page(astronaut)
                # create empty dictionary
                astro_data = {}

                astro_data['url'] = astro.url
                astro_data['summary'] = wikipedia.summary(astronaut)
                # then add it to the dictionary
                self.astro_dict[astronaut] = astro_data
                # save dictionary
                self._save()
            except wikipedia.exceptions.PageError:
                # do nothing
                pass
            except wikipedia.exceptions.DisambiguationError:
                pass

    def get_data(self):
        # return copy of current dictionary
        return self.astro_dict.copy()


if __name__ == '__main__':
    ad = AstronautDictionary('./data.json')
    x = None
    # get list of all astronauts
    astronauts = requests.get('http://api.open-notify.org/astros.json').json()
    # fetch the data
    for astronaut in astronauts['people']:
        ad.set_data(astronaut['name'])

    astronauts = ad.get_data()
    for astronaut in astronauts:
        name = format_name(astronaut, False)
        print(f"\n{name}\n{astronauts[astronaut]['summary']}\n{astronauts[astronaut]['url']}")
