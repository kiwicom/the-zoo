"""Link to docs: http://docs.gunicorn.org/en/stable/settings.html."""

worker_class = "gevent"

bind = ":8080"

accesslog = "-"  # send access log to stdout
