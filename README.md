# Persim
A tool for generating HTTP/REST docs in Markdown from Yaml

Swagger may cause confusion. A persim berry might help with that

## TODO

- [x] Load yml files as a dict
- [ ] Add `globals` where they belong
    - [ ] request_headers
    - [ ] response_headers
    - [x] responses
- [x] Add `vars` where they belong
- [ ] Sort the parsed dict
- [ ] Render the parsed dict to markdown
    - [ ] Path arguments
    - [x] Everything else
- [x] Write it to something

## Usage

Yaml parsed by this tool has 3 main sections, `globals`, `vars`, and `routes`.

### Globals

`globals` are common pieces of information that are a part of every request of some method, and are added to each of those. As of yet, planned supported globals are
    - request_headers: for headers that are a part of a request
    - response_headers: for headers that are a part of a responses
    - responses: responses that any endpoint can return

`globals` can be specified in the following tree. Keep in mind that `method` may be a specific method, or a wildcard to be added to all methods

```YAML
<type>:
    <method>:
        foo
```

Any time that a global is shadowed by a manually inserted value. For example where there is a document that looks like so:

```YAML
globals:
    responses:
        "*":
            404: foo

routes:
    /:
        GET:
            ...
            responses:
                404: bar
```

the global 404 will not be added into the response for `GET /`

### Vars

`vars` are variables. They can be nested and accessed using dot notation. To reference a variable, prefix the value with a `$`

For example the following YAML

```YAML
vars:
    response:
        get_root:
            lang: JSON
            content: {"online": true}

routes:
    /:
        GET:
            ...
            responses:
                200: $response.get_root
```

would render in the same way as

```YAML
routes:
    /:
        GET:
            ...
            responses:
                200:
                    lang: JSON
                    content: {"online": true}
```

### Routes

`routes` are the primary content of the yaml, and what is rendered. A basic outline looks like this

```YAML
routes:
    <route>:
        <method>:
            description: route description
            path_arguments:
                - list of
                - path arguments
            headers:
                - list of
                - headers
            query_strings:
                - list of
                - query strings
            body: request body, if any
            responses:
                code: response pairs
```

They take supplementing fields that look like these

__headers, path arguments, and query strings__

```YAML
object:
    name: field name
    value: field value
    required: true | false
```

They look the same, just put them in the right place

__body__

```YAML
body:
    lang: language for markdown syntax highlighting
    content: body content
```

__response__

```YAML
code:
    title: response title
    description: response description
    body: response body
```

The body is in the same format as the body of a request
