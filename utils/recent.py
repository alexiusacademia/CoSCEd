import os
import json


class Recent:
    """
    Handles the recent projects feature
    """
    FILE_NAME_RECENT = 'recent.dat'

    def __init__(self):
        # Create a recent json file if not exist
        path = os.path.join(os.getcwd(), self.FILE_NAME_RECENT)
        exists = os.path.isfile(path)
        if not exists:
            # Create it
            self.create_recent_file()

    def create_recent_file(self):
        fn = os.path.join(os.getcwd(), self.FILE_NAME_RECENT)
        data = {'recent': []}
        with open(fn, 'w') as output_file:
            json.dump(data, output_file, indent=4)

    def add_recent(self, path):
        pass

    def get_recent(self):
        """
        Get the list of recent projects
        :return:
        """
        pass