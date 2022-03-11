## Project generation and updating, or re-generating

This project was generated using https://github.com/tiangolo/full-stack-fastapi-postgresql with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql
```

You can check the variables used during generation in the file `cookiecutter-config-file.yml`.

You can generate the project again with the same configurations used the first time.

That would be useful if, for example, the project generator (`tiangolo/full-stack-fastapi-postgresql`) was updated and you wanted to integrate or review the changes.

You could generate a new project with the same configurations as this one in a parallel directory. And compare the differences between the two, without having to overwrite your current code but being able to use the same variables used for your current project.

To achieve that, the generated project includes the file `cookiecutter-config-file.yml` with the current variables used.

You can use that file while generating a new project to reuse all those variables.

For example, run:

```console
$ cookiecutter --config-file ./cookiecutter-config-file.yml --output-dir ../project-copy https://github.com/tiangolo/full-stack-fastapi-postgresql
```

That will use the file `cookiecutter-config-file.yml` in the current directory (in this project) to generate a new project inside a sibling directory `project-copy`.
