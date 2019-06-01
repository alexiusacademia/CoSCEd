import json


class FileOperation:
    """
    Collection of file operations for the
    application.
    """
    filename = ''

    def __init__(self, fn):
        """
        Constructor specifying the project filename.
        :param fn: Project filename
        """
        self.filename = fn

    def get_json(self):
        """
        Load the project file as json object.
        :return: Project json object.
        """
        project_file = open(self.filename, 'r')
        project_file_lines = project_file.readlines()
        json_string = ''
        for line in project_file_lines:
            json_string += line
        json_project = json.loads(json_string)
        return json_project

    def save_json(self, data):
        """
        Saves the json object to file.
        :param data: The json object to save.
        :return:
        """
        with open(self.filename, 'w') as output_file:
            json.dump(data, output_file, indent=4)
