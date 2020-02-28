let pkgs = import <nixpkgs> {};
    version="1.0.dev0";
    base = import ./base.nix {inherit version pkgs;};
in base.overrideAttrs (self: rec {
  buildInputs = self.buildInputs ++ [
    pkgs.yarn
    pkgs.postgresql
  ];

  exportVarsHook=''
    export DJANGO_SETTINGS_MODULE=zoo.base.settings
    export ZOO_DEBUG=true
  '';

  yarnHook = ''
     function process_assets {
      say "Running yarn && webpack"
      cd $PROJ_HOME/webpack

      yarn install --frozen-lockfile && \
           yarn cache clean

      if [ -d source ]; then
        rm -rf source
      fi

      cp -r $PROJ_HOME/zoo source
      yarn production

      cd $PROJ_HOME

      say "Running django-admin collectstatic"
      django-admin collectstatic --noinput > /dev/null
    }

    say "To process js/css assets please execute shellc command process_assets !"
  '';

  databaseHook = ''
    export PGDATA=$PWD/.postgres/data
    export PGSOCKET=$PWD/.postgres/socket
    export LOG_PATH=$PWD/.postgres/LOG
    export PGDATABASE=postgres
    export DATABASE_URL="postgres://localhost/postgres"

    if [ ! -d $PGHOST ]; then
       mkdir -p $PGHOST
    fi
    if [ ! -d $PGSOCKET ]; then
       mkdir -p $PGSOCKET
    fi
    if [ ! -d $PGDATA ]; then
       say "Initializing postgresql databse"
       initdb $PGDATA --auth=trust > /dev/null
    fi

    say_green "Starting postgres database"
    pg_ctl start -l $LOG_PATH -D $PGDATA -o "-c unix_socket_directories=$PGSOCKET"
    trap "pg_ctl stop" EXIT
  '';

  shellHook=self.shellHook + ''
     ${exportVarsHook}
     ${yarnHook}
     ${databaseHook}
  '';
})
