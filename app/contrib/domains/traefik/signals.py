

def update_traefik_config(sender, instance, **kwargs):
    instance.update_traefik_config()


def delete_traefik_config(sender, instance, **kwargs):
    instance.delete_traefik_config()