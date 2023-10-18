# Shell Options
set shell := ["bash", "-eo pipefail"]
set dotenv-load

# Project Settings
project := "io-control"
package :=  "iocontrol"

# List recipes.
default:
    #!/usr/bin/env bash
    echo {{package}}
    just --list


# Build a project item.
build target:
    #!/usr/bin/env bash
    if [ "{{target}}" = "ui" ]; then
        pushd "./{{project}}/api/static"
        find . ! -name '.gitkeep' -type f -exec rm -f {} +
        rm -Rf -- */
        popd
        pushd ui
        npm run build
        popd
        cp -R ./ui/build/* "./{{project}}/api/static/"
        exit 0
    fi
    echo Assuming "{{target}}" refers to a Docker container.
    path="docker/images/$(echo {{target}} | tr '-' '/')"
    if [ ! -f "$path/justfile" ]; then
        >&2 echo "$path/justfile does not exist."
        exit 1
    fi
    pushd "$path"
    # Build the image.
    just build


# Compile the application.
compile:
    #!/usr/bin/env bash
    source venv/bin/activate
    cp pyproject.toml {{package}}
    python -m nuitka \
      --include-package={{package}} \
      --include-package-data={{package}} \
      --onefile \
      --output-dir=dist \
      --run \
      --standalone \
      --static-libpython=no \
      -o {{project}}.bin \
      compile.py
    mv dist/{{project}}.bin dist/{{project}}
    rm {{package}}/pyproject.toml

# Install Docker.
docker:
    #!/usr/bin/env bash
    # Run the pyenv install script for this operating system.
    pushd scripts/{{os()}}/docker
    bash install.sh
    popd

# Lint code with flake8
flake8:
    #!/usr/bin/env bash
    source venv/bin/activate
    flake8 {{package}}
    flake8 tests

# Install GDAL.
gdal:
    #!/usr/bin/env bash
    # Run the pyenv install script for this operating system.
    pushd scripts/{{os()}}/gdal
    bash install.sh
    popd


# Install dependencies.
install:
    #!/usr/bin/env bash
    source venv/bin/activate
    poetry install

# Log in to a running Docker container.
login target user='nonroot':
    #!/usr/bin/env bash
    path="docker/images/$(echo {{target}} | tr '-' '/')"
    if [ ! -f "$path/justfile" ]; then
        >&2 echo "$path/justfile does not exist."
        exit 1
    fi
    pushd "$path"
    just login {{user}}
    popd

# Prettify the code to comply with the linter.
black:
    #!/usr/bin/env bash
    source venv/bin/activate
    echo Prettifying {{package}}...
    black {{package}}
    echo Prettifying unit tests...
    black tests

# Start a Docker container in this project.
down target:
    #!/usr/bin/env bash
    set -euo pipefail
    path="docker/images/$(echo {{target}} | tr '-' '/')"
    if [ ! -f "$path/justfile" ]; then
        >&2 echo "$path/justfile does not exist."
        exit 1
    fi
    pushd "$path"
    just down
    popd

# Run pre-commit against all files in the project.
pre-commit:
    #!/usr/bin/env bash
    source venv/bin/activate
    pre-commit run --all-files

# Prettify the code.
prettify: reorder-python-imports black

# Install pyenv.
pyenv:
    #!/usr/bin/env bash
    # Run the pyenv install script for this operating system.
    pushd scripts/{{os()}}/pyenv
    bash install.sh
    popd

# Install nvm.
nvm:
    #!/usr/bin/env bash
    cp .nvmrc scripts/{{os()}}/nvm
    pushd scripts/{{os()}}/nvm
    bash install.sh
    popd

# Prepare the environment.
ready: venv gdal
    #!/usr/bin/env bash
    # Perform platform specific steps.
    case "{{os()}}" in
      macos*)   ;;
      linux*)   sudo apt-get install ccache patchelf ;;
      windows*) raise error "Windows is not yet supported." ;;
      *)        raise error "Unknown OS: {{os()}}" ;;
    esac
    source venv/bin/activate
    if [ -e .env ]
    then
        printf '.env already exists.\n'
    else
        touch just.env
        printf 'Created .env.\n'
    fi
    pip install pip --upgrade
    pip install poetry
    poetry install
    just install
    pre-commit install
    # Create the starter config file.
    {{package}} config create

# Run unit tests.
pytest:
    #!/usr/bin/env bash
    source venv/bin/activate
    pytest --cov={{project}} tests/

# Re-order python imports.
reorder-python-imports:
    #!/usr/bin/env bash
    source venv/bin/activate
    find "./{{package}}" -type f -name '*.py' -exec reorder-python-imports "{}" \;

# Start the service.
start:
    #!/usr/bin/env bash
    source venv/bin/activate
    {{package}} api start

# Build Sphinx documentation.
sphinx:
    #!/usr/bin/env bash
    source venv/bin/activate
    pushd sphinx
    rm source/apidoc/*.rst
    make html
    popd

# Open an SSH session to a container.
ssh target user='nonroot':
    #!/usr/bin/env bash
    set -euo pipefail
    path="docker/images/$(echo {{target}} | tr '-' '/')"
    if [ ! -f "$path/justfile" ]; then
        >&2 echo "$path/justfile does not exist."
        exit 1
    fi
    pushd "$path"
    just ssh {{user}}
    popd

# Create a virtual environment.
venv: pyenv
    #!/usr/bin/env bash
    if [ -e venv ]
    then
        printf 'There is already a virtual environment here.\n'
    else
        eval "$(pyenv init -)"
        cat .python-version | pyenv install
        python3 -m venv venv
        printf 'Created a virtual environment (venv).\n'
        source venv/bin/activate
        python --version
    fi

# Start a Docker container in this project.
up target:
    #!/usr/bin/env bash
    set -euo pipefail
    path="docker/images/$(echo {{target}} | tr '-' '/')"
    if [ ! -f "$path/justfile" ]; then
        >&2 echo "$path/justfile does not exist."
        exit 1
    fi
    pushd "$path"
    just up
    popd

# Find dead code.
vulture:
    #!/usr/bin/env bash
    source venv/bin/activate
    vulture {{package}}/
