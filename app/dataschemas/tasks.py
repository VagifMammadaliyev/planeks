from celery import shared_task

from planeks.celery import QUEUES
from dataschemas.models import DataSet


@shared_task(queue=QUEUES.GENERATOR_QUEUE)
def generate_csv(dataset_id):
    dataset = DataSet.objects.filter(id=dataset_id).first()
    if not dataset:
        return f"Dataset with id {dataset_id} not found"
    total_seconds = dataset.generate()
    return f"Generated {dataset.row_count} rows in {total_seconds} seconds"
