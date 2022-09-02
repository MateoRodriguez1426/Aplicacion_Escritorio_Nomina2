from cProfile import label
from email import message
from inspect import Parameter
#from sys import last_value
from tkinter import ttk
from tkinter import *
import sqlite3
from unicodedata import name

class product: 
    
    db_name = 'database.db'
    
    
    
    #Clase Nomina
    def __init__(self, window):         #Constructor que hace que cada vez que se inicia la clase, ejecute una instancia que le de nombre a la ventana de la aplicacion  
        self.wind = window
        self.wind.title('Register Employees')
        
        #Aqui se va a crear el frame es decir el lugar donde se van a  poder acomodar lo elemetos
        frame = LabelFrame(self.wind, text = 'Register a new Employee')
        frame.grid(row = 0, column = 0, columnspan= 3, pady=20)
        
        #Entrada de datos/input  = Nombre
        
        
        Label(frame, text = 'Name: ').grid(row =1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column = 1)
        
        #Apellidos
        
        Label(frame, text = 'Last Name: ').grid(row =2, column = 0)
        self.lname = Entry(frame)
        self.lname.grid(row=2, column = 1)
        
        #Documento de Identidad
        Label(frame, text = 'Id Document: ').grid(row =3, column = 0)
        self.document = Entry(frame)
        self.document.grid(row=3, column = 1)
        
        
        #Salario
        Label(frame, text = 'Basic Wage: ').grid(row =4, column = 0)
        self.wage = Entry(frame)
        self.wage.grid(row=4, column = 1)
        
        #Dias Trabajados
        Label(frame, text = 'Worked Days: ').grid(row =5, column = 0)
        self.workdays = Entry(frame)
        self.workdays.grid(row=5, column = 1)
        
      
        #Boton Entrada de Productos
        ttk.Button(frame, text= ' Register Employee ', command=self.add_product).grid(row = 6, columnspan= 2, sticky =W + E)
        

        #Mensajes de alerta
        self.message = Label(text='', fg = 'red')
        self.message.grid(row = 3, column=0, columnspan= 2, sticky= W+E)
        
        #Tabla
        self.tree = ttk.Treeview(height = 10, columns= ('#1', '#2', '#3','#4','#5','#6', '#7', '#8', '#9'))
        self.tree['show'] = 'headings'
        self.tree.grid(row = 7, column = 0, columnspan = 6)
        self.tree.heading('#1', text = 'Name', anchor= CENTER)
        self.tree.heading('#2', text = 'LastName', anchor= CENTER)
        self.tree.heading('#3', text = 'Id Document', anchor= CENTER)
        self.tree.heading('#4', text = 'Wage', anchor= CENTER)
        self.tree.heading('#5', text = 'Worked Days', anchor= CENTER)
        self.tree.heading('#6', text = 'Pension', anchor= CENTER)
        self.tree.heading('#7', text = 'Salud', anchor= CENTER)
        self.tree.heading('#8', text = 'Subsidio Transporte', anchor= CENTER)
        self.tree.heading('#9', text = 'Salario Neto', anchor= CENTER)
        
        
        
        
        #Botones tabla
        ttk.Button(text = 'DELETE', command=self.delete_employee).grid(row = 8, column=2, sticky= W + E)
        ttk.Button(text = 'EDIT', command=self.edit_employees).grid(row = 8, column=3, sticky= W + E) 
        
        
        self.get_employees()
       
       
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result =  cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_employees (self):
        #lIMPIAR TABLE
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        #query
        query = 'SELECT * FROM employees ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[0])
            
            
    def validation(self):
        return len(self.name.get()) != 0 and len(self.lname.get()) != 0       
    
    
    
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO employees VALUES (?, ?)'
            parameters = (self.name.get(), self.lname.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Empleado {} agregado exitosamente'.format(self.name.get())
            self.name.delete(0, END)
            self.lname.delete(0, END)
        
        else:
            self.message['text'] = 'Nombre y Precio son requeridos'
        self.get_employees()
        
        
        
    def delete_employee(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Porfavor elija un empleado para eliminar su registro'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM employees WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Registro {} eliminado satisfactoriamente'.format(name)
        self.get_employees()


    def edit_employees(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection() )['text'][0]
        except IndexError as e:
            self.message ['text'] = 'Por favor seleccione un Registro'
            return
        Name = self.tree.item(self.tree.selection())['text']
        LastName= self.tree.item(self.tree.selection())['text']
        Id_Document = self.tree.item(self.tree.selection())['text']
        Wage =  self.tree.item(self.tree.selection())['text']
        Worked_Days = self.tree.item(self.tree.selection())['text']

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar producto'


        #Viejos datos
        Label(self.edit_wind, text = 'Nombre Anterior: ').grid(row = 0, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=name), state ='readonly').grid (row = 0, column=2)

        #Nuevos Datos
        Label(self.edit_wind, text= 'Nuevo Nombre').grid(row = 1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        #Viejos datos
        Label(self.edit_wind, text = 'Ultimo Apellido Registrado: ').grid(row = 2, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=LastName), state ='readonly').grid (row = 2, column=2)

        #Nuevos Datos
        Label(self.edit_wind, text= 'Nuevo Apellido').grid(row = 3, column=1)
        new_lname = Entry(self.edit_wind)
        new_lname.grid(row=3, column=2)


        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_lname.get(), LastName)).grid(row = 4, column= 2, sticky = W+E)


        def edit_records(self, new_name, name, new_lname, lname):
            query = 'UPDATE employees SET name = ?, lname = ? WHERE name = ? AND lname = ?'
            parameters = (new_name, new_lname, name, lname)
            self.run_query(query, parameters)
            self.edit_wind.destroy()
            self.message ['text'] = 'Registro {} Modificado satisfactoriamente'.format(name)
            self.get_employees()

if __name__ == '__main__':
    window = Tk()
    application = product (window)
    window.mainloop() 
