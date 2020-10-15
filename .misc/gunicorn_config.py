"""Link to docs: http://docs.gunicorn.org/en/stable/settings.html."""

from gunicorn.glogging import Logger


class CustomLogger(Logger):
    def access(self, resp, req, environ, request_time):
        """Do not log if User Agent is present within the ignore list."""
        ignore_user_agents = ["kube-probe"]

        headers = {name.lower(): value for name, value in req.headers}
        request_user_agent = headers.get("user-agent", "")

        for agent in ignore_user_agents:
            if request_user_agent.startswith(agent):
                return

        super().access(resp, req, environ, request_time)


worker_class = "gevent"

bind = ":8080"

accesslog = "-"  # send access log to stdout

logger_class = CustomLogger
