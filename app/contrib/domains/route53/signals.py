

def delete_on_route53(sender, instance, **kwargs):
    instance.delete_on_route53()