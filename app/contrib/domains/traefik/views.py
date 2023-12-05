from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

# import etcd
from etcd3 import Client

# Fazer pre configuração

configs = [
    # Setup inicial
    (
        "traefik/tls/options/default/cipherSuites/0",
        "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
    ),
    (
        "traefik/tls/options/default/cipherSuites/1",
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    ),
    (
        "traefik/tls/options/default/cipherSuites/2",
        "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
    ),
    (
        "traefik/tls/options/default/cipherSuites/3",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
    ),
    (
        "traefik/tls/options/default/cipherSuites/4",
        "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305",
    ),
    (
        "traefik/tls/options/default/cipherSuites/5",
        "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305",
    ),
    ("traefik/tls/options/default/minVersion", "VersionTLS12"),
    ("traefik/http/middlewares/securityHeader/headers/contenttypenosniff", "true"),
    ("traefik/http/middlewares/securityHeader/headers/framedeny", "false"),
    ("traefik/http/middlewares/securityHeader/headers/sslredirect", "true"),
    ("traefik/http/middlewares/securityHeader/headers/stsincludesubdomains", "true"),
    ("traefik/http/middlewares/securityHeader/headers/stspreload", "true"),
    ("traefik/http/middlewares/securityHeader/headers/stsseconds", "63072000"),
]


def create_initial_config(request):
    client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
    
    for config in configs:
        client.put(key=config[0], value=config[1])
    
    return HttpResponse("Config is OK!")


def get_all_traefik_config(request):
    client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)

    # try:
    resp = client.range("traefik/http/routers/", prefix=True)
    import ipdb;ipdb.set_trace()
    # except etcd.EtcdKeyNotFound:
    #     import ipdb;ipdb.set_trace()
        # for config in configs:
        #     client.write(config[0], config[1])

    return render(request, "traefik/settings.html")

cms_configs = [
    ("traefik/http/routers/cms-config/tls", "true"),
    ("traefik/http/routers/cms-config/tls/certresolver", "myresolver"),
    ("traefik/http/routers/cms-config/service", "cms@docker"),
    # 
    ("traefik/http/routers/cms-config/rule", "HostRegexp(`cms.staging.bonde.org`)"),
    # ("traefik/http/services/cms/loadbalancer/server/port", 8000),
]

def create_cms_config(request):
    #   - traefik.http.routers.cms.priority=10
    #   - traefik.http.services.cms.loadbalancer.server.port=8000
    #   - traefik.http.routers.cms.tls=true
    #   - traefik.http.routers.cms.tls.certresolver=myresolver
    #   - traefik.http.routers.cms.rule=${TRAEFIK_ROUTERS_RULE:-HostRegexp(`cms.staging.bonde.org`)}

    client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
    
    for config in cms_configs:
        client.put(key=config[0], value=config[1])
    
    return HttpResponse("Config is OK!")


public_base_configs = [
    ("traefik/http/routers/public-0/tls", "true"),
    ("traefik/http/routers/public-0/tls/certresolver", "myresolver"),
    ("traefik/http/routers/public-0/service", "webpage@docker"),
    # 
    # Configura todas as entradas possíveis
    ("traefik/http/routers/public-0/rule", "HostRegexp(`{host:.+}`)"),
    ("traefik/http/routers/public-0/tls/domains/0/main", "staging.bonde.org"),
    ("traefik/http/routers/public-0/tls/domains/0/sans/0", "*.staging.bonde.org"),
]

def create_public_config(request):
    client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
    
    for config in public_base_configs:
        client.put(key=config[0], value=config[1])
    
    return HttpResponse("Config is OK!")


def delete_public_config(request):
    client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
    
    for config in public_whoami_configs:
        client.delete_range(key=config[0])
    
    return HttpResponse("Config is OK!")


public_whoami_configs = [
    ("traefik/http/routers/public-config-testes/tls", "true"),
    ("traefik/http/routers/public-config-testes/tls/certresolver", "myresolver"),
    ("traefik/http/routers/public-config-testes/service", "cms@docker"),
    # 
    # Configura todas as entradas possíveis
    ("traefik/http/routers/public-config-testes/rule", "HostRegexp(`sub.whoami.staging.bonde.org`, `www.sub.whoami.staging.bonde.org`)"), 
    ("traefik/http/routers/public-config-testes/tls/domains/0/main", "whoami.staging.bonde.org"),
    ("traefik/http/routers/public-config-testes/tls/domains/0/sans/0", "*.whoami.staging.bonde.org"),
]


def create_whoami_config(request):
    client = Client(host=settings.ETCD_HOST, port=settings.ETCD_PORT)
    
    for config in public_whoami_configs:
        client.put(key=config[0], value=config[1])
    
    return HttpResponse("Config is OK!")
