# Utils Package Manager System

All code should be modular, and since the beginning of times, this task is accomplished using libraries. Problem is, libraries can get too massive, and many times, only a portion of them is needed.

It is also very common to have an "utils" file with source code defining auxiliary tasks that are written more than once in a lifetime, because they are not worth modularizing in libraries.

That is where `upm` comes into play. The idea is to have a **minimal** package manager that manages those portions of code needed by your code with no need to write them again on demand.

### Definitions

- A **package** is a portion of code
- A **portion of code** is a set of tasks
- A **task** is a function in a programming language

### Goals

- `upm` must be **unobtrusive**, this means, it must be compatible with the structure of any project, and must not ask for special formatting to its users
- Code pieces (or packages) must be minimal and atomic, this means, it must not be necessary to keep track of package versions, since each package is defined as a set of immutable tasks

**Important:** Each task's (function's) *behaviour* and *signature* should be immutable once commited, but new tasks could be added since it would not break the package's functionality

### Developing language support

Language support files should be located under `mod/lang/{lang_code}.py`, and must implement all functions inside `mod/lang/__interface__.py`