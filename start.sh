#!/usr/bin/env sh
set -eu

if [ -f "app/entrypoint.py" ]; then
  exec python app/entrypoint.py
fi

if [ -f "api-baldas-blog/app/entrypoint.py" ]; then
  cd api-baldas-blog
  exec python app/entrypoint.py
fi

echo "Cannot find app/entrypoint.py. Check Koyeb root directory/start command." >&2
exit 1

