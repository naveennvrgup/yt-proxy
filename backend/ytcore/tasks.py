from celery import shared_task



@shared_task
def helloworld():
    print("celery hello world")


@shared_task
def query_yt():
    print("celery hello world")