#!/usr/bin/env bash
su postgres <<'EOF'
dropdb stoychevart
createdb -O stoychevart stoychevart
EOF