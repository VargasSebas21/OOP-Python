import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5 import uic
from Empresa import *


class MainWindowEmpresa(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("Gui/Ventana_Principal.ui", self)
        self.setFixedSize(self.size())
        self.dialogo_registrar_cliente = DialogoRegistrarCliente()
        self.dialogo_registrar_empleado = DialogoRegistrarEmpleado()
        self.dialogo_eliminar_cliente = DialogoEliminarCliente()
        self.dialogo_cambiarplan_cliente = DialogoCambiarPlan()
        self.empresa =Empresa()
        self.__configurar()


    def __configurar(self):
        # Configurar el QlistView
        self.Ventanita.setModel(QStandardItemModel())


        # Enlazar eventos de los botones
        self.Registrar_Cliente.clicked.connect(self.abrir_dialogo_registrar_cliente)
        self.Registrar_Empleado.clicked.connect(self.abrir_dialogo_registrar_empleado)
        self.Eliminar_Cliente.clicked.connect(self.abrir_dialogo_eliminar_cliente)
        self.Cambiar_Paquete.clicked.connect(self.abrir_dialogo_cambiarplan_cliente)

    def __cargar_clientes(self):
        clientes = list(self.empresa.Clientes.values())
        for cliente in clientes:
            item = QStandardItem(str(cliente))
            item.setEditable(False)
            self.Ventanita.model().appendRow(item)

    def abrir_dialogo_registrar_cliente(self):
        resp = self.dialogo_registrar_cliente.exec_()
        if resp == QDialog.Accepted:
            nombre = self.dialogo_registrar_cliente.Nombre.text()
            identificacion = self.dialogo_registrar_cliente.Identificacion.text()
            telefono = self.dialogo_registrar_cliente.Telefono.text()
            Gmail = self.dialogo_registrar_cliente.Gmail.text()
            fecha_ingreso = str(self.dialogo_registrar_cliente.Fecha_Ingreso.text())
            Plan = self.dialogo_registrar_cliente.Plan.text()
            try:
                cliente = self.empresa.registrar_cliente(identificacion, nombre, telefono, Gmail, fecha_ingreso, Plan)
            except ClienteExistenteError as err:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("ERROR")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText(err.mensaje)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
            else:
                model = self.Ventanita.model()
                item = QStandardItem(str(cliente))
                item.setEditable(False)
                model.appendRow(item)
        self.dialogo_registrar_cliente.limpiar()

    def abrir_dialogo_cambiarplan_cliente(self):
        resp = self.dialogo_cambiarplan_cliente.exec_()
        if resp == QDialog.Accepted:
            nuevoplan = self.dialogo_cambiarplan_cliente.NuevoPlan.text()
            identificacion = self.dialogo_cambiarplan_cliente.Identi.text()

            try:
                self.empresa.cambiar_plan(identificacion, nuevoplan)
            except ClienteNoExistenteError as err:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("ERROR")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText(err.mensaje)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Cambiar Plan")
                msg_box.setText("Se ha efectuado el cambio correctamente")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                self.Ventanita.model().clear()
                self.__cargar_clientes()

        self.dialogo_cambiarplan_cliente.limpiar()

    def abrir_dialogo_eliminar_cliente(self):
        resp = self.dialogo_eliminar_cliente.exec_()
        if resp == QDialog.Accepted:

            identificacion = self.dialogo_eliminar_cliente.EliminarCliente.text()

            try:
                self.empresa.eliminar_cliente(identificacion)
            except ClienteNoExistenteError as err:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("ERROR")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText(err.mensaje)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
            else:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Eliminar Cliente")
                msg_box.setText("Se ha eliminado correctamente")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                self.Ventanita.model().clear()
                self.__cargar_clientes()



        self.dialogo_eliminar_cliente.limpiar()

    def abrir_dialogo_registrar_empleado(self):
        resp = self.dialogo_registrar_empleado.exec_()
        if resp == QDialog.Accepted:
            identificacion = self.dialogo_registrar_empleado.Identificacion.text()
            nombre = self.dialogo_registrar_empleado.Nombre.text()
            Cargo = self.dialogo_registrar_empleado.Cargo.text()

            try:
                self.empresa.registrar_empleado(identificacion, nombre, Cargo)
            except EmpleadoExistenteError as err:
                 msg_box = QMessageBox(self)
                 msg_box.setWindowTitle("ERROR")
                 msg_box.setIcon(QMessageBox.Warning)
                 msg_box.setText(err.mensaje)
                 msg_box.setStandardButtons(QMessageBox.Ok)
                 msg_box.exec_()
            else:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Registro Empleado")
                msg_box.setText("Se ha registrado correctamente")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
        self.dialogo_registrar_empleado.limpiar()



class DialogoRegistrarCliente(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Gui/DialogoRegistrarCliente.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):
        self.Telefono.setValidator(QRegExpValidator(QRegExp("\\d{10}"), self.Telefono))
        self.Identificacion.setValidator(QRegExpValidator(QRegExp("\\d{11}"), self.Identificacion))
        self.Nombre.setValidator(QRegExpValidator(QRegExp("[a-zA-Z]*"),self.Nombre))

    def limpiar(self):
        self.Gmail.clear()
        self.Telefono.clear()
        self.Nombre.clear()
        self.Identificacion.clear()
        self.Plan.clear()


    def accept(self) -> None:
        if self.Identificacion.text() != "" and self.Nombre.text() != "" and self.Telefono.text() != "" and self.Gmail.text()!="" and self.Plan.text() != "":
            super(DialogoRegistrarCliente, self).accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("ERROR")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Por favor ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

class DialogoRegistrarEmpleado(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Gui/DialogoRegistrarEmpleado.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):

        self.Identificacion.setValidator(QRegExpValidator(QRegExp("\\d{11}"), self.Identificacion))
        self.Nombre.setValidator(QRegExpValidator(QRegExp("[a-zA-Z]*"),self.Nombre))

    def limpiar(self):

        self.Cargo.clear()
        self.Nombre.clear()
        self.Identificacion.clear()



    def accept(self) -> None:
        if self.Identificacion.text() != "" and self.Nombre.text() != "" and self.Cargo.text() != "":
            super(DialogoRegistrarEmpleado, self).accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("ERROR")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Por favor ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

class DialogoCambiarPlan(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Gui/DialogoCambiarPlan.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):

        self.Identi.setValidator(QRegExpValidator(QRegExp("\\d{11}"), self.Identi))
        self.NuevoPlan.setValidator(QRegExpValidator(QRegExp("[a-zA-Z]*"),self.NuevoPlan))

    def limpiar(self):


        self.NuevoPlan.clear()
        self.Identi.clear()



    def accept(self) -> None:
        if self.Identi.text() != "" and self.NuevoPlan.text() != "":
            super(DialogoCambiarPlan, self).accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("ERROR")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Por favor ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()


class DialogoEliminarCliente(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Gui/DialogoEliminarCliente.ui", self)
        self.setFixedSize(self.size())
        self.__configurar()

    def __configurar(self):

        self.EliminarCliente.setValidator(QRegExpValidator(QRegExp("\\d{11}"), self.EliminarCliente))


    def limpiar(self):


        self.EliminarCliente.clear()



    def accept(self) -> None:
        if self.EliminarCliente.text() != "":
            super(DialogoEliminarCliente, self).accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("ERROR")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Por favor ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowEmpresa()
    win.show()
    sys.exit(app.exec_())
