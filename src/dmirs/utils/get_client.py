from dmirs.models import Client


def get_client(db_identifier):
    return Client.objects.get(db_id=db_identifier)
