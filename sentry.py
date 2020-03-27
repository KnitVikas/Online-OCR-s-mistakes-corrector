import subprocess
import sentry_sdk
from sentry_sdk import capture_exception as capex
import os


def insertSentryRelease():
    try:
        curr_commit_ = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        curr_commit_ = str(curr_commit_.strip())[2:-1]
        to_insert = "\nSENTRY_RELEASE=spell-corrector@" + curr_commit_
        with open(".env", "r") as envf:
            lines = (
                "".join(
                    [
                        line
                        for line in envf.readlines()
                        if not line.startswith("SENTRY_RELEASE")
                    ]
                ).rstrip()
                + to_insert
            )
        with open(".env", "w") as envf:
            for line in lines:
                envf.write(line)
    except:
        # to_insert = "\nSENTRY_RELEASE=sectioned-analyzer@1.0.0"
        with open(".env", "w") as envf:
            envf.write("SENTRY_RELEASE=spell-corrector@1.0.0")


def sentryMain():
    sentry_dsn = os.getenv("SENTRY_DSN")
    sentry_sdk.init(
        dsn=sentry_dsn, max_breadcrumbs=90, debug=False, attach_stacktrace=True
    )
    sentry_env = (
        os.getenv("SENTRY_ENVIRONMENT") == "production"
    )  # Two values : production or development, in production mode sentry_env=True
    # print(f"sentry_env : {sentry_env}")
    insertSentryRelease()
    return sentry_env
