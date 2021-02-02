{ version, pkgs ? import <nixpkgs> {}}:
with pkgs;
with pkgs.postgresql_12;
with pkgs.python38Packages;

stdenv.mkDerivation rec {
  name = "the-zoo";

  buildInputs = [
    glibcLocales
    python
    poetry
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

    ${__helperFuncs}

    say "Initializing development environment"

    if [ ! -d $VENV ]; then
      say_green "Initializing virtualenv environment ($VENV)"
      virtualenv $VENV > /dev/null
    fi

    say_green "Activating virtualenv ($VENV)"
    source $PWD/$VENV/bin/activate

    say_green "Installing requirements"
    poetry install

    if [ -f setup.py ]; then # if setup.py exists switch to develop mode
      say "setup.py found!"
      say "Switching to development mode"
      python setup.py develop > /dev/null
    fi
  '';
}
