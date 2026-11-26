#!/bin/bash

set -e

if [[ -z "${PYCSW_HARVESTERS:-}" ]]; then
    echo "PYCSW_HARVESTERS must be set to one or more CONFIG|URL pairs" >&2
    exit 1
fi

touch /home/pycsw/data/cron.log
echo "Installing cron job..."

cron_file=$(mktemp)
trap 'rm -f "$cron_file"' EXIT
minute=0

IFS=';' read -r -a harvesters <<< "$PYCSW_HARVESTERS"
for harvester in "${harvesters[@]}"; do
    if [[ "$harvester" != *'|'* ]]; then
        echo "Invalid PYCSW_HARVESTERS entry: expected CONFIG|URL, got '$harvester'" >&2
        exit 1
    fi

    config=${harvester%%|*}
    url=${harvester#*|}
    if [[ -z "$config" || -z "$url" ]]; then
        echo "Invalid PYCSW_HARVESTERS entry: config and URL are required" >&2
        exit 1
    fi

    /venv/bin/pycsw-admin.py setup-repository --config "$config"
    printf '%d 0 * * * /venv/bin/pycsw-admin.py refresh-harvested-records --config %q --url %q >> /home/pycsw/data/cron.log 2>&1\n' \
        "$minute" "$config" "$url" >> "$cron_file"
    minute=$(((minute + 5) % 60))
done

crontab "$cron_file"

# Start cron service
service cron start

# Print cron status for debugging
echo "Cron service status:"
service cron status

# Show installed cron jobs
echo "Installed cron jobs:"
crontab -l || echo "No cron jobs installed"

tail -f /home/pycsw/data/cron.log
