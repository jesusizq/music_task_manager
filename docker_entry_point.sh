#!/bin/bash

usage() {
    echo "Usage: $0 --env-file PATH_TO_ENV [--skip-run]"
    echo
    echo "Options:"
    echo "  --env-file PATH      Specify the path to the .env file (required)"
    echo "  --skip-run           Skip running the Flask application"
    exit 1
}

SKIP_RUN=false
ENV_FILE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-run) SKIP_RUN=true ;;
        --env-file)
            if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
                ENV_FILE="$2"
                shift
            else
                echo "Error: --env-file requires a valid path."
                usage
            fi
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
            ;;
    esac
    shift
done

if [ -z "$ENV_FILE" ]; then
    echo "Error: --env-file is required."
    usage
fi

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

poetry run flask db upgrade

if [ "$SKIP_RUN" = false ]; then
    poetry run flask run
fi
