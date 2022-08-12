import json
import requests
import conf

sandbox = "https://10.10.20.14"
cabecera = {
    "Content-Type": "application/json"
}


def obtener_token():
    url = sandbox + "/api/aaaLogin.json"
    body = {
        "aaaUser": {
            "attributes": {
                "name": conf.usuario,
                "pwd": conf.clave
            }
        }
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False)
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token']

    return token


galletin = {
    "APIC-Cookie": obtener_token()
}


def consulta_api():
    respuesta = requests.get(sandbox + "/api/class/topSystem.json", headers=cabecera, cookies=galletin, verify=False)
    return respuesta.json()


def crear_tenant():
    tenant_1 = {
        "fvTenant": {
            "attributes": {
                "name": "TenantX"
            }
        }
    }
    tenant_1 = json.dumps(tenant_1, indent=4)
    tenant = requests.post(sandbox + "/api/mo/uni.json", headers=cabecera, cookies=galletin, verify=False,
                           data=tenant_1)
    return tenant.status_code


def interfaces():
    interface = requests.get(sandbox + "/api/node/mo/topology/pod-1/node-101/sys/phys-[eth1/1].json", headers=cabecera,
                             cookies=galletin, verify=False)
    return interface.json()


print(obtener_token())
print(consulta_api())
print(crear_tenant())
print(interfaces())