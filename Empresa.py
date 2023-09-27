import csv


class Cliente:

    def __init__(self, identificacion, nombre, telefono, gmail, fecha_ingreso, Plan=""):
        self.identificacion = identificacion
        self.nombre = nombre
        self.telefono = telefono
        self.gmail = gmail
        self.fecha_ingreso = fecha_ingreso
        self.Plan = Plan
    def cambiar_paquete(self, plan):
        self.Plan = plan

    def __str__(self):
        return "[{}], ({}, {}, {}, {}, {})  ".format (self.identificacion, self.nombre, self.telefono, self.gmail, self.fecha_ingreso, self.Plan)





class Empleado:

    def __init__(self, identificacion, nombre, Posicion_Empresa):
        self.identificacion = identificacion
        self.nombre = nombre
        self.Posicion_empresa = Posicion_Empresa
class Empresa:

    def __init__(self):
        self.Empleados = {}
        self.Clientes = {}

    def __Cargar_clientes(self):
        with open("data/clientes.csv") as file:
            csv_data = csv.reader(file, delimeter = ";")
            cliente = map(lambda data: Cliente(data[0] , data[1], data[2], data[3], data[4],data[5] ),csv_data)
            self.Clientes = {cli.identificacion:cli for cli in cliente}

    def registrar_cliente(self, identificacion, nombre, telefono, gmail, fecha_ingreso, Plan):
        if not self.client_exists(identificacion):
            cliente = Cliente(identificacion, nombre, telefono, gmail, fecha_ingreso, Plan)
            self.Clientes[identificacion] = cliente
            return cliente
        else:
            raise ClienteExistenteError(identificacion, "Ya existe un usuario registrado con esta identificación")

    def client_exists(self, identificacion):
        return identificacion in self.Clientes.keys()

    def registrar_empleado(self, identificacion, nombre, Posicion_empresa):
        if not self.employee_exists(identificacion):
            empleado = Empleado(identificacion, nombre, Posicion_empresa)
            self.Empleados[identificacion] = empleado
        else:
            raise EmpleadoExistenteError(identificacion, "Ya existe un empleado registrado con esta identificación")

    def employee_exists(self, identificacion):
        return identificacion in self.Empleados.keys()

    def eliminar_cliente(self, identificacion):
        if self.client_exists(identificacion):
           del self.Clientes[identificacion]
        else:
            raise ClienteNoExistenteError(identificacion, "No existe cliente con ese numero de identificacion")

    def consultar_plan(self, identificacion):
        if self.client_exists(identificacion):
            cliente = self.Clientes[identificacion]
            return cliente.Plan
        else:
            raise ClienteNoExistenteError(identificacion, "No existe cliente con ese numero de identificacion")

    def cambiar_plan(self, identificacion, plan):
        if self.client_exists(identificacion):
            cliente = self.Clientes[identificacion]
            cliente.cambiar_paquete(plan)
        else:
            raise ClienteNoExistenteError(identificacion, "No existe cliente con ese numero de identificacion")





class Empresa_Error(Exception):
    pass


class ClienteExistenteError(Empresa_Error):

    def __init__(self, identificacion, mensaje):
        self.identificacion = identificacion
        self.mensaje = mensaje


class ClienteNoExistenteError(Empresa_Error):

    def __init__(self, identificacion, mensaje):
        self.identificacion = identificacion
        self.mensaje = mensaje
class EmpleadoExistenteError(Empresa_Error):

    def __init__(self, identificacion, mensaje):
        self.identificacion = identificacion
        self.mensaje = mensaje