#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
PROJECT_ROOT=$(dirname "${SCRIPT_DIR}")
MINICONDA_ROOT=${PROJECT_ROOT}/.miniconda
VENV_NAME="translator"

# step 1: download miniconda

# architecture possible values: x86_64, arm64
architecture="$(uname -m)"
uname_output="$(uname -s)"
case "${uname_output}" in
    Linux*)     download_url="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-${architecture}.sh";;
    Darwin*)    download_url="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-${architecture}.sh";;
    *)          download_url="UNKNOWN:${uname_output}"
esac

echo "Downloading miniconda installer from ${download_url}"
wget ${download_url} -O ${SCRIPT_DIR}/miniconda.sh

# step 2: install miniconda
#-b           run install in batch mode (without manual intervention),
#             it is expected the license terms are agreed upon;
#             does not edit shell scripts such as .bashrc, .bash_profile, .zshrc, etc.
#-f           force installation even if prefix -p already exists.
#-h           print this help message and exit
#-p PREFIX    install prefix, defaults to ${HOME}/miniconda3, must not contain spaces.
#-s           skip running pre/post-link/install scripts
#-u           update an existing installation
#-t           run package tests after installation (may install conda-build)
bash ${SCRIPT_DIR}/miniconda.sh -b -p ${MINICONDA_ROOT}

# step 3: create virtual env `${VENV_NAME}` and provision it
# https://anaconda.org/conda-forge/
CONDA_FORGE_PACKAGES=(
  "html2text"
  "markdown"
  "markupsafe"
  "openai"
  "tiktoken"
  "tqdm"
)

${MINICONDA_ROOT}/bin/conda create --name ${VENV_NAME} --channel conda-forge --yes python=3.10
${MINICONDA_ROOT}/bin/conda install --name ${VENV_NAME} --channel conda-forge --yes ${CONDA_FORGE_PACKAGES[*]}


# Using PIP directly is necessary until M1 hardware is fully supported by the pytorch channel of miniconda
PIP_PACKAGES=(
)
if [ -n "${PIP_PACKAGES}" ]; then
  # PIP_PACKAGES list is not empty
  ${MINICONDA_ROOT}/envs/${VENV_NAME}/bin/pip3 install ${PIP_PACKAGES[*]}
fi

rm ${SCRIPT_DIR}/miniconda.sh
