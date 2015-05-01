#!/usr/bin/env bash
su postgres <<'EOF'
dropdb signali
createdb -O signali signali
EOF