#!/bin/bash
exec gunicorn -b :8100  --access-logfile - --error-logfile -  "generator:create_app()"