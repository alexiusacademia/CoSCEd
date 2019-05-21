import os
import json


class Recent:
    """
    Handles the recent projects feature
    """
    FILE_NAME_RECENT = 'recent.dat'
    full_path = ''

    def __init__(self):
        # Create a recent json file if not exist
        self.full_path = os.path.join(os.getcwd(), self.FILE_NAME_RECENT)
        exists = os.path.isfile(self.full_path)
        if not exists:
            # Create it
            self.create_recent_file()

    def create_recent_file(self):
        fn = os.path.join(os.getcwd(), self.FILE_NAME_RECENT)
        data = {'recent': []}
        with open(fn, 'w') as output_file:
            json.dump(data, output_file, indent=4)

    def add_recent(self, path):
        recent_projects = self.get_recent()
        if path in recent_projects:
            pass
        else:
            recent_projects.append(path)
        data = {'recent': recent_projects}

        fn = os.path.join(os.getcwd(), self.FILE_NAME_RECENT)
        with open(fn, 'w') as output_file:
            json.dump(data, output_file, indent=4)

    def get_recent(self):
        """
        Get the list of recent projects
        :return:
        """
        recent_file = open(self.full_path, 'r')

        proj_file_lines = recent_file.readlines()
        json_string = ''

        for line in proj_file_lines:
            json_string += line

        recent_json = json.loads(json_string)
        return recent_json['recent']