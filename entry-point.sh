#!/usr/bin/env bash

# Copyright (c) Datalayer, Inc https://datalayer.io
# Distributed under the terms of the MIT License.

if [ "$DB_LOCAL_START" == "true" ]
then
    echo
    echo Starting Local Posgresql Server
    sudo -u postgres /usr/lib/postgresql/10/bin/postgres \
        -D /var/lib/postgresql/10/main \
        -c config_file=/etc/postgresql/10/main/postgresql.conf &
    sleep 5
fi

echo
echo Starting Crossplane Examples Python Server [host:$DB_HOST username:$DB_USERNAME]
python3 -m crossplane_examples
