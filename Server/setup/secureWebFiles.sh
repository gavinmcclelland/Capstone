#!/usr/bin/env bash
# Lockdown the public web files
find /var/www -exec chown wi-wait:www-data {} \;
find /var/www -type d -exec chmod -v 750 {} \;
find /var/www -type f -exec chmod -v 640 {} \;
