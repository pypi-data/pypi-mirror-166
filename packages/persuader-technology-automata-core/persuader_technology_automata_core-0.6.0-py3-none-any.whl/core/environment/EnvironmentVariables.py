import os


class EnvironmentVariables:

    def __init__(self):
        self.options = self.parse_environment_variables(os.environ.items())

    @staticmethod
    def parse_environment_variables(environment_vars):
        options = {}
        for k, v in environment_vars:
            # todo: could ignore specific values
            options[k] = v
        return options

    def url(self):
        return self.options['URL'] if 'URL' in self.options else None
