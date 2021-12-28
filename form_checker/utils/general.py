from toml import load as toml_load


project_data = toml_load("pyproject.toml")


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


def get_project_attribute(*paths):
    data = project_data
    for path in paths:
        data = data[path]
    return data
