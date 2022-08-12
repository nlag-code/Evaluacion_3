import json
import requests
import conf

sandbox = "https://10.10.20.14"
cabecera = {
    "Content-Type": "application/json"
}


def obtener_token(): # Generamos la funcion para obtener el token.
    url = sandbox + "/api/aaaLogin.json" #Generamos la url de acuerdo a lo que nos indica la documentacion.
    body = { #Segun la documentacion le pasamos nuestras credenciales utilizando la estructura Json, estras credenciales las obtenemos desde el lab de cisco.
        "aaaUser": {
            "attributes": {
                "name": conf.usuario,
                "pwd": conf.clave
            }
        }
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False)
    #Hacemos un get entregando la cabecera definida mas arriba, en la data entregaremos las credenciales en formato json y desactivamos la verificacion.
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token']
    #Como ya hemos visto en clase, recorreremos la respuesta obtenida solamente para guardar el token en la variable token.
    return token # al llamar a nuestra funcion esta nos entregará la variable token.


galletin = {
    "APIC-Cookie": obtener_token()
}


def consulta_api():
    respuesta = requests.get(sandbox + "/api/class/topSystem.json", headers=cabecera, cookies=galletin, verify=False)
    return respuesta.json()


def crear_tenant():
    tenant_1 = { # Generamos la variable tenant_1 la cual tendrá la info necesaria para la creación de nuestro tenant, en este caso pasamos la información basica en argumentos que es el nombre del tenant.
        "fvTenant": {
            "attributes": {
                "name": "TenantX"
            }
        }
    }
    tenant_1 = json.dumps(tenant_1) # Pasamos la variable tenant a formato Json para que a la hora de la consulta esta pueda ser leida.
    tenant = requests.post(sandbox + "/api/mo/uni.json", headers=cabecera, cookies=galletin, verify=False,
                           data=tenant_1) # Siguiendo la documentacion, debemos hacer un post para entregar la data para la creacion del tenant, en cookies indicamos la variable galletin que a su vez llama al token, en la variable data entregamos la informacion para crear nuestro tenant.
    return tenant.status_code # para validar que la creacion fue exitosa, en este caso estamos retornando el status_code del metodo post anterior.


def interfaces():
    interface = requests.get(sandbox + "/api/node/mo/topology/pod-1/node-101/sys/phys-[eth1/1].json", headers=cabecera,
                             cookies=galletin, verify=False) # para obtener informacion utilizamos el metodo get, siguiendo la misma estructura anterior, en la url indicaremos el nodo y la interfaz a la cual le haremos la consulta.
    print(interface.request.headers)
    print(interface.headers)
    return interface.json() # nuestra funcion retornara la data de la interfaz a la cual le hicimos el get.


print(obtener_token())
print(consulta_api())
print(crear_tenant())
print(interfaces())


