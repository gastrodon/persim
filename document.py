import yaml

class Document:
    def __init__(self, content):
        self._doc = yaml.safe_load(content)
        self._global_parser_map = {
            "responses": self._parse_globals_responses,
            "request_headers": self._parse_globals_request_headers
        }

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
        for name in section:
            val = section[name]
            if isinstance(val, dict):
                section[name] = self._get_var_dict(val)

            if isinstance(val, str):
                section[name] = self._get_var(val)

            if isinstance(val, list):
                section[name] = self._get_var_list(val)

        return section

    def parse_variables(self):
        self._doc["globals"] = self._get_var_dict(self.globals)
        self._doc["routes"] = self._get_var_dict(self.routes)
        return self

                valid = [v for v in valid if len(v)]

    def parse_globals(self):
        for name in self.globals:
            self._global_parser_map[name]()

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
