aprompt
=======

**A**dvanced **Prompt**s replace the built-in
`input()` with colored and optimized prompts.
Note that using aprompt inside an IDE will
probably not work.


Features
--------

- [x] text
- [x] password
- [x] amount
- [x] select
- [x] multi-select
- [ ] path _(available in the future)_
- [x] custom formatter _(not documented yet)_
- [x] custom prompts _(not documented yet)_
- [ ] repeat\_while _(not entirely implemented yet)_
- [ ] detailed docs


Usage
-----

```python
import itertools
import aprompt as ap

name = ap.prompt(
    "Please enter your name.",
    ap.prompts.text()
)

age = ap.prompt(
    "Please enter your age.",
    ap.prompts.amount(
        minimum = 0,
        maximum = 150,
    ),
    repeat_while = lambda x: x < 18
)

password = ap.prompt(
    "Please enter your password.",
    ap.prompts.text(hide = True)
)

language = ap.prompt(
    "What language do you prefer?",
    ap.prompts.select(
        "English",
        "Chinese",
        "French",
        "Japanese",
        "German"
    )
)

can_code_in = ap.prompt(
    "In what languages can you code in?",
    ap.prompts.select(
        "c",
        "c++",
        "c#",
        "python",
        "ruby",
        "javascript",
        "java",
        "pascal",
        "haskell",
        "rust",
        "go",
        "lua",
        "swift",
        "R",
        "bash",
        sort = True,
        multiple = True,
        require = itertools.count(1)
    )
)


```