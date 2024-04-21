from fastapi import FastAPI
#from flask_cors import CORS
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from models.MMs import MM1, MMs,Costos, MM1K
from utils.Response import Response
from fastapi.responses import JSONResponse


app = FastAPI()

# Configuración de políticas CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "localhost:3000",
                   "http://localhost:3000", "http://localhost:3000/",
                   "https://trafico-y-cola.vercel.app/", 
                   "https://trafico-y-cola.vercel.app"],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Origin",
        "Accept",
        "X-Requested-With",
        "Content-Type",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "Access-Control-Allow-Origin",
    ],
)


def factorial(n):
    return 1 if (n == 1 or n == 0) else n * factorial(n - 1)

def get_values_mms(request_body, no_server = 0):
    lamb = request_body.lamb
    miu = request_body.miu
    s = request_body.number_servers

    basic_values = {}
    second_value = 0
    #formula para hallar roo
    basic_values['p'] = lamb/(s*miu)
    rho = basic_values['p']

    s_factorial = factorial(s)
    first_value = (((lamb/miu)**s)/s_factorial)*((s*miu)/(s*miu-lamb))
    
    print(f"n: valor")
    for i in range (0, s, 1):
        value = ((lamb/miu)**i)/factorial(i)
        print(f"{i}:  {value}")
        second_value = second_value + value     

    basic_values['p0'] =  round(1/(first_value+second_value),3)

    if no_server != 0:
        rho = lamb/(no_server*miu)

    #numero promedio de clientes en la cola lq
    basic_values['lq'] = round(((1/s_factorial)*((lamb/miu)**s)*(rho/(1-rho)**2))*basic_values['p0'],3)

    basic_values['ls'] = round(basic_values['lq']+(lamb/miu),3)
    basic_values['wq'] = round(basic_values['lq']/lamb,3)
    basic_values['ws'] = round(basic_values['wq']+(1/miu),3)

    for key, value in basic_values.items():
        basic_values[key] = float(value)

    return basic_values


def get_values_mm1(request_body):
    lamb = request_body.lamb
    miu = request_body.miu

    basic_values = {}
    #formula para hallar roo
    basic_values['p'] = lamb/miu 
    
    basic_values['p0'] = 1-basic_values['p']

    #numero promedio de clientes en la cola lq
    basic_values['lq'] = round((lamb**2)/(miu*(miu-lamb)),4)

    basic_values['ls'] = round(basic_values['p']/basic_values['p0'],4)
    basic_values['wq'] = round(lamb/(miu*(miu-lamb)),4)
    basic_values['ws'] = round(1/(miu-lamb),4)

    for key, value in basic_values.items():
        basic_values[key] = float(value)

    return basic_values


def get_values_mm1k(request_body):
    lamb = request_body.lamb
    miu = request_body.miu
    k = request_body.k

    basic_values = {}
    #formula para hallar roo
    basic_values['p'] = lamb/miu 
    
    #valores necesarios
    k1 = k+1
    pk = basic_values['p']**k
    pk1 = basic_values['p']**k1
    
    basic_values['p0'] = (1-basic_values['p'])/(1-pk1)

    #numero promedio de clientes en la cola lq
    basic_values['l'] = round((basic_values['p']/(1-basic_values['p']))-((k1*pk1)/(1-pk1)),4)
    basic_values['lambda_prima'] = round(lamb*(1-((1-3)*pk)/(1-pk1)),4)
    basic_values['w'] = round(basic_values['l']/basic_values['lambda_prima'],4)
    basic_values['wq'] = round(basic_values['w']-(1/miu),4)
    basic_values['lq'] = round(basic_values['lambda_prima']*basic_values['wq'],4)

    for key, value in basic_values.items():
        basic_values[key] = float(value)

    return basic_values


@app.post("/mm1-analysis")
def compute_mm1(MM1_values: MM1 = Body(...)):
    basic_values = get_values_mm1(MM1_values)

    #return Response.success(data=[basic_values], message="hola")
    return {"message":"hola"}


@app.post("/mms-analysis")
def compute_mms(MMs_values: MMs = Body(...)):
    basic_values = get_values_mms(MMs_values)

    return Response.success(data=[basic_values], message="MMs values found")


@app.post("/mms-costos-analysis")
def compute_mms_costos(Costos_values: Costos = Body(...)):
    n = 6
    costos_values = []
    
    basic_values = get_values_mms(Costos_values)
    costos_values.append(basic_values)

    number_servers = Costos_values.number_servers

    for i in range(number_servers,n+1,1):
        Costos_values.number_servers = i

        basic_values = get_values_mms(Costos_values, number_servers)
        basic_values['e_cs'] = float(i*Costos_values.service_cost)
        basic_values['e_cw'] = float(Costos_values.wait_cost*basic_values['ls'])
        basic_values['e_ct'] = float(basic_values['e_cs'] + basic_values['e_cw'])

        costos_values.append(basic_values)

    return Response.success(data=[costos_values], message="MMs-Costos values found")


@app.post("/mm1k-analysis")
def compute_mm1k(MM1k_values: MM1K = Body(...)):
    basic_values = get_values_mm1k(MM1k_values)

    print(type(basic_values))

    return Response.success(data=[basic_values], message="MM1k values found")

# @app.post("/mms-costos-analysis")
# def register_person(person: Person = Body(...)):
#     new_person = {"name": person.first_name, "email": person.email}
#     new_person["password"] = f.encrypt(person.password.encode("utf-8"))
#     conn.execute(users.insert().values(new_person))
#     #Conectar a la BD
#     return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()