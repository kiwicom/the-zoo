"""Link to docs: http://docs.gunicorn.org/en/stable/settings.html"""
import os

workers = os.environ.get("WEB_CONCURRENCY", 1)

bind = ":8080"

accesslog = "-"  # send access log to stdout
