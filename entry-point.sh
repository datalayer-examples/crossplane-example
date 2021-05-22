#!/usr/bin/env bash

# Copyright (c) Datalayer, Inc https://datalayer.io
# Distributed under the terms of the MIT License.

if [ "$DB_LOCAL_START" == "true" ]
then
    echo Starting Local Posgresql Server
    sudo -u postgres /usr/lib/postgresql/10/bin/postgres \
        -D /var/lib/postgresql/10/main \
        -c config_file=/etc/postgresql/10/main/postgresql.conf &
    sleep 10
fi

echo Starting Crossplane Examples Python Server with database host $DB_HOST and database username $DB_USERNAME

python3 -m crossplane_examples
