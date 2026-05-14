from app.scheduler.scheduler import configure_daily_digest_job


class FakeScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, func, trigger: str, **kwargs):
        self.jobs.append(
            {
                "func": func,
                "trigger": trigger,
                "kwargs": kwargs,
            }
        )


def test_configure_daily_digest_job_registers_daily_malaysia_time_job():
    scheduler = FakeScheduler()

    configure_daily_digest_job(
        scheduler=scheduler,
        job_func=lambda: None,
        hour=8,
        minute=0,
        timezone="Asia/Kuala_Lumpur",
    )

    assert len(scheduler.jobs) == 1
    job = scheduler.jobs[0]
    assert job["trigger"] == "cron"
    assert job["kwargs"]["hour"] == 8
    assert job["kwargs"]["minute"] == 0
    assert job["kwargs"]["timezone"] == "Asia/Kuala_Lumpur"
    assert job["kwargs"]["id"] == "daily_news_digest"
