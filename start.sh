#!/bin/bash

set -e

function usage() {
  cat <<@
  Single script to install / translate

  Usage: $0 (install|translate)
    * install      create virtual env and initialize the secrets.py file
    * translate    run the translation
@
  exit 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

if [[ "$(uname)" == "Darwin" ]]; then
  function realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
  }
fi


ACTION=${1}
if [[ ${ACTION} = "install" ]]; then
  ./scripts/install_virtualenv.sh

  cat <<EOF >secrets.py
import os

API_SECRET_KEY = os.environ.get('OPENAI_API_KEY', '***YOUR-OPENAI-API-KEY***')
API_ENDPOINT = os.environ.get('OPENAI_API_ENDPOINT', 'https://api.openai.com/v1')
API_VERSION = os.environ.get('OPENAI_API_VERSION', None)
EOF

elif [[ ${ACTION} = "translate" ]]; then
  if [[ $# -lt 3 ]]; then
    cat <<@
  Follow the format below for *translate* action

  Usage: $0 translate book_details

  for instance:
  $0 translate doomed_city
@
    exit 1
  fi

  # ${@:2} skips names of this script and the name of the "translate" command
  .miniconda/bin/conda run --name translator python translator.py "${@:2}"

else
  echo "ERROR: Unknown action ${ACTION}."
  usage
  exit 1
fi
