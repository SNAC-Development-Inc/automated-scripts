# automated-scripts

scripts for automating tasks

# Developer setup

## Versions

- Minimum Python version 3.10.7

## VSCode Extensions

- Applescripts

## Cloning the Repository

- I like to clone the repository via the https URL, you will have to setup a github PAT (personal access token) to do this, your personal token will expire after a time so you have reset ever so often

## Environment

- make sure your terminal is pointed to this project folder `automated-scripts`
- If you do not have mise-en-place installed:
  - Install mise-en-place https://mise.jdx.dev/getting-started.html#_1-install-mise-cli
  - Restart terminal
  - Run
    - `mise trust`
    - `mise i`
- Mise place willl handle setting our python version for us via venv
- run `python -m venv .venv` to setup the .venv folder

- Google Sheets/Docs API setup

  - https://developers.google.com/sheets/api/quickstart/python
  - https://developers.google.com/docs/api/quickstart/python
  - Install google api python packages

## Environment variables

- add to this file the following variables based on your machine
- PATH_TO_CREDENTIALS_JSON=
- add path to your credentials json file to google sheets
