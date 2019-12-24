import yaml

class Document:
    def __init__(self, content):
        self._doc = yaml.safe_load(content)

    def _get_var(self, name):
        var = self.vars

        if not name.startswith("$") or not len(name) - 1:
            return name

        for sub in name[1:].split("."):
            var = var.get(sub, {})

        return var

    def _get_var_list(self, names):
        for index in range(len(names)):
            name = names[index]

            if isinstance(name, str):
                names[index] = self._get_var(name)

            if isinstance(name, list):
                names[index] = self._get_var_list(name)

            if isinstance(name, dict):
                names[index] = self._get_var_dict(name)

        return names

    def _get_var_dict(self, section):
        for key in section:
            val = section[key]
            if isinstance(val, dict):
                section[key] = self._get_var_dict(val)

            if isinstance(val, str):
                section[key] = self._get_var(val)

            if isinstance(val, list):
                section[key] = self._get_var_list(val)

        return section

    def parse_variables(self):
        self._doc["routes"] = self._get_var_dict(self.routes)
        return self

    @property
    def routes(self):
        return self._doc.get("routes", {})

    @property
    def vars(self):
        return self._doc.get("vars", {})

    @property
    def globals(self):
        return self._doc.get("globals", {})