import os
import json
from utils.file_op import FileOperation


class Recent:
    """
    Handles the recent projects feature
    """
    FILE_NAME_RECENT = 'recent.dat'
    filename = ''
    file_op = None

    def __init__(self):
        # Create a recent json file if not exist
        self.filename = os.path.join(os.getcwd(), self.FILE_NAME_RECENT)

        exists = os.path.isfile(self.filename)
        if not exists:
            # Create it
            self.create_recent_file()

        self.file_op = FileOperation(self.filename)

    def create_recent_file(self):
        data = {'recent': []}
        self.file_op.save_json(data)

    def add_recent(self, path):
        recent_projects = self.get_recent()
        if path in recent_projects:
            recent_projects.append(recent_projects.pop(recent_projects.index(path)))
        else:
            recent_projects.append(path)
        data = {'recent': recent_projects}

        self.file_op.save_json(data)

    def get_recent(self):
        """
        Get the list of recent projects
        :return:
        """
        recent_json = self.file_op.get_json()

        return recent_json['recent']
