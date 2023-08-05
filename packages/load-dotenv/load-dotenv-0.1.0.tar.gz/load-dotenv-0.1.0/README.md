# load-dotenv
Environment variables are a great and popular way to configure your application.
Although the number of such variables can be really high in a big application, making
it annoying to manage during development.

Common solution for this issue is usage of `.env` files which contain all variables
that should be loaded into your development environment. There are different ways
to do this, for example handy [python-dotenv](https://pypi.org/project/python-dotenv/)
package. But it should be executed explicitly in order to work. In my projects
I don't want to add `load_dotenv()` execution in my code that is running on
production, and I'm too lazy to create customer runners for development only.
Thus, I made **load-dotenv** that can do this for me automatically.

## Installation
```shell
pip install load-dotenv
```

## Usage
Create `.env` file in your working directory and put your variables there.
For details about file format, please refer
[python-dotenv documentation](https://saurabh-kumar.com/python-dotenv/#file-format).
Run your application with `LOAD_DOTENV` variable set to one of `true`, `yes` or `1`.

Alternative path to the file can be specified via `LOAD_DOTENV_PATH` variable.
