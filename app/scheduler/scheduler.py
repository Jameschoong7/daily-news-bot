from collections.abc import Callable

from apscheduler.schedulers.blocking import BlockingScheduler

from app.main import main

DEFAULT_TIMEZONE = "Asia/Kuala_Lumpur"
DEFAULT_HOUR = 8
DEFAULT_MINUTE = 0


def configure_daily_digest_job(
    scheduler: BlockingScheduler,
    job_func: Callable[[], None],
    hour: int = DEFAULT_HOUR,
    minute: int = DEFAULT_MINUTE,
    timezone: str = DEFAULT_TIMEZONE,
) -> None:
    """Register the daily news digest job on a scheduler."""
    scheduler.add_job(
        job_func,
        "cron",
        hour=hour,
        minute=minute,
        timezone=timezone,
        id="daily_news_digest",
        replace_existing=True,
    )


def run_scheduler() -> None:
    """Start the blocking scheduler for daily digest delivery."""
    scheduler = BlockingScheduler(timezone=DEFAULT_TIMEZONE)
    configure_daily_digest_job(scheduler=scheduler, job_func=main)
    scheduler.start()


if __name__ == "__main__":
    run_scheduler()
