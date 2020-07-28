import celery

from data_workflow_api import celery_tasks


@pytest.fixture(scope='module')
def celery_tasks(request):
    celery_tasks.conf.update(CELERY_ALWAYS_EAGER=True)
    return celery_tasks

    