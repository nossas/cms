from django.apps import AppConfig
# from django.db.models.signals import post_save, post_delete
# from django.conf import settings


# from etcd3 import Client

# initial_config = [
#     # Setup inicial
#     (
#         "traefik/tls/options/default/cipherSuites/0",
#         "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
#     ),
#     (
#         "traefik/tls/options/default/cipherSuites/1",
#         "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
#     ),
#     (
#         "traefik/tls/options/default/cipherSuites/2",
#         "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
#     ),
#     (
#         "traefik/tls/options/default/cipherSuites/3",
#         "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
#     ),
#     (
#         "traefik/tls/options/default/cipherSuites/4",
#         "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305",
#     ),
#     (
#         "traefik/tls/options/default/cipherSuites/5",
#         "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305",
#     ),
#     ("traefik/tls/options/default/minVersion", "VersionTLS12"),
#     ("traefik/http/middlewares/securityHeader/headers/contenttypenosniff", "true"),
#     ("traefik/http/middlewares/securityHeader/headers/framedeny", "false"),
#     ("traefik/http/middlewares/securityHeader/headers/sslredirect", "true"),
#     ("traefik/http/middlewares/securityHeader/headers/stsincludesubdomains", "true"),
#     ("traefik/http/middlewares/securityHeader/headers/stspreload", "true"),
#     ("traefik/http/middlewares/securityHeader/headers/stsseconds", "63072000"),
# ]


# initial_web_application_config = [
#     ("traefik/http/routers/0-public-staging-bonde-org/tls", "true"),
#     ("traefik/http/routers/0-public-staging-bonde-org/tls/certresolver", "myresolver"),
#     ("traefik/http/routers/0-public-staging-bonde-org/service", "webpage@docker"),
#     # Configura todas as entradas possíveis
#     ("traefik/http/routers/0-public-staging-bonde-org/rule", "HostRegexp(`{host:.+}`)"),
#     ("traefik/http/routers/0-public-staging-bonde-org/tls/domains/0/main", "staging.bonde.org"),
#     ("traefik/http/routers/0-public-staging-bonde-org/tls/domains/0/sans/0", "*.staging.bonde.org"),
# ]


class TraefikAppConfig(AppConfig):
    name = "contrib.domains.traefik"

    # def ready(self):
    #     import os
        
    #     if not os.getenv("DISABLE_TRAEFIK", False):
    #         client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)

    #         configs = []
    #         configs.extend(initial_config)
    #         configs.extend(initial_web_application_config)

    #         for key_value in configs:
    #             client.put(key=key_value[0], value=key_value[1])


    #     # Signals configuration
    #     from . import signals, models

    #     post_save.connect(signals.update_traefik_config, sender=models.Route)
    #     post_delete.connect(signals.delete_traefik_config, sender=models.Route)
