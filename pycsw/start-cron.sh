#!/bin/bash
set -e

touch /home/pycsw/data/cron.log
cd /home/pycsw/data && /venv/bin/pycsw-admin.py setup-repository --config $PYCSW_CONFIG

echo "Installing cron job..."
crontab /etc/cron.d/harvester

# Start cron service
service cron start

# Print cron status for debugging
echo "Cron service status:"
service cron status

# Show installed cron jobs
echo "Installed cron jobs:"
crontab -l || echo "No cron jobs installed"

tail -f /home/pycsw/data/cron.log
