from collections import namedtuple
from typing import Dict


class SentryRater:
    RATE_LIMIT = 60 * 60 * 24

    def __init__(self, daily_events: int, issues: namedtuple, *args, **kwargs):
        self.daily_events = daily_events
        self.issues = issues

        rate_limit_reason = """
            {percentage} of the rate limit reached, that's {comparison}. Come on, we can do better 💪🏻
            """

        self.available_grades = {
            "S": f"""{self.issues.total} issues found… but none of them seem problematic!
                    Right on track, as it should be 👍🏻""",
            "A": f"""{self.issues.total} issues found, and {self.issues.problematic} of them seem problematic.
                    Not too bad, but it can be better 😊""",
            "B": f"""{self.issues.total} issues found, and {self.issues.problematic} of them need to be handled 🧐
                    Come on, we can do better 💪🏻""",
            "C": f"""{self.issues.total} issues found, and {self.issues.stale} of them are stale.
                    These issues usually indicate someting broken by design. Come on, we can do better 💪🏻""",
            "D": rate_limit_reason,
            "E": rate_limit_reason,
            "F": rate_limit_reason,
        }

    def according_to_event_count(self) -> Dict[str, str]:
        if self.daily_events / self.RATE_LIMIT >= 0.9:
            return {
                "grade": "F",
                "reason": self.available_grades["F"].format(
                    percentage="90%", comparison="one event per second"
                ),
            }

        if self.daily_events / self.RATE_LIMIT >= 0.5:
            return {
                "grade": "E",
                "reason": self.available_grades["E"].format(
                    percentage="50%", comparison="30 errors every minute"
                ),
            }

        if self.daily_events / self.RATE_LIMIT >= 0.1:
            return {
                "grade": "D",
                "reason": self.available_grades["D"].format(
                    percentage="10%", comparison="one error every 10 seconds"
                ),
            }

        return None

    def according_to_issue_count(self) -> Dict[str, str]:
        if self.issues.problematic == 0:
            grade = "S"
        elif (
            self.issues.spoiled < 10
            and self.issues.decaying < 5
            and self.issues.stale == 0
        ):
            grade = "A"
        elif self.issues.stale <= 10 and self.issues.total <= 100:
            grade = "B"
        else:
            grade = "C"

        return {"grade": grade, "reason": self.available_grades[grade]}

    def get_rating(self) -> Dict[str, str]:
        return self.according_to_event_count() or self.according_to_issue_count()
