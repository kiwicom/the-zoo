{ version, pkgs ? import <nixpkgs> {}}:
with pkgs;
with pkgs.python38Packages;

stdenv.mkDerivation rec {
  name = "the-zoo";

  buildInputs = [
    glibcLocales
    python
    virtualenv
  ];

  __helperFuncs = ''
    SOURCE_DATE_EPOCH=$(date +%s)
    YELLOW='\033[1;33m'
    GREEN='\033[1;32m'
    NC="$(printf '\033[0m')"
    PROJ_HOME=$PWD
    VENV=".venv"

    function say {
      echo -e "''${YELLOW}$1...''${NC}"
    }

    function say_green {
      echo -e "''${GREEN}$1''${NC}"
    }
  '';

  shellHook = ''
    unset PYTHONPATH

    export LANG=en_US.UTF8
    export PACKAGE_VERSION=${version}
    export PIP_CONFIG_FILE=$PWD/.pip.conf

    echo "[global]
no-cache-dir = true" > $PWD/.pip.conf

    ${__helperFuncs}

    say "Initializing development environment"

    if [ ! -d $VENV ]; then
      say_green "Initializing virtualenv environment ($VENV)"
      virtualenv $VENV > /dev/null
    fi

    say_green "Activating virtualenv ($VENV)"
    source $PWD/$VENV/bin/activate

    say_green "Installing requirements"
    REQS=""
    if [ -f "requirements.txt" ]; then # By default checks if requirements.txt exists
      REQS="-r requirements.txt"
    fi

    for f in *-requirements.txt; do # Search for dev-requirements.txt, doc-requirements.txt etc.
        REQS="''${REQS} -r ''${f}"
    done

    if [ -d requirements ]; then # for pip-compile-multi requirements are in a requirements folder
      for f in requirements/*.txt; do
          REQS="''${REQS} -r ''${f}"
      done
    fi
    pip install $REQS > /dev/null # install all requirements collected

    if [ -f setup.py ]; then # if setup.py exists switch to develop mode
      say "setup.py found!"
      say "Switching to development mode"
      python setup.py develop > /dev/null
    fi
  '';
}
