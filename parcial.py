import tkinter as tk
from tkinter import messagebox
import random
import time
from threading import Thread

class Sensor:
    def __init__(self):
        self.temperatura = 0
        self.humedad = 0
        self.activo = False
        self.umbral_alerta = 30  
        self.historial = []  
        
    def generar_datos(self):
        try:
            
            self.temperatura = round(random.uniform(0, 50), 1)
            self.humedad = round(random.uniform(20, 90), 1)
            
            
            if self.temperatura < 0 or self.humedad < 0:
                raise ValueError("Valor negativo generado")
                
            
            registro = {
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'temperatura': self.temperatura,
                'humedad': self.humedad,
                'alerta': self.temperatura > self.umbral_alerta
            }
            self.historial.append(registro)
            
            
            if len(self.historial) > 100:
                self.historial.pop(0)
                
        except Exception as e:
            print(f"Error al generar datos: {e}")
           
            self.temperatura = 25
            self.humedad = 50
    
    def simular_lecturas(self):
        self.activo = True
        while self.activo:
            self.generar_datos()
            time.sleep(2)  
    
    def detener_lecturas(self):
        self.activo = False
    
    def set_umbral(self, valor):
        try:
            self.umbral_alerta = float(valor)
            return True
        except ValueError:
            return False


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        self.sensor = Sensor()
        
       
        self.hilo_sensor = Thread(target=self.sensor.simular_lecturas, daemon=True)
        self.hilo_sensor.start()
        
       
        self.configurar_interfaz()
        
        
        self.actualizar_datos()
        
       
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def configurar_interfaz(self):
       
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        
        tk.Label(main_frame, text="Monitor de Sensores", font=('Arial', 16, 'bold'), 
                bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        
        datos_frame = tk.LabelFrame(main_frame, text="Datos del Sensor", bg='#f0f0f0', padx=10, pady=10)
        datos_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
       
        tk.Label(datos_frame, text="Temperatura:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=0, sticky='e')
        self.lbl_temp = tk.Label(datos_frame, text="0.0 °C", font=('Arial', 12), bg='#f0f0f0')
        self.lbl_temp.grid(row=0, column=1, sticky='w', padx=(10, 20))
        
        tk.Label(datos_frame, text="Humedad:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='e')
        self.lbl_hum = tk.Label(datos_frame, text="0.0 %", font=('Arial', 12), bg='#f0f0f0')
        self.lbl_hum.grid(row=1, column=1, sticky='w', padx=(10, 20))
        
       
        umbral_frame = tk.LabelFrame(main_frame, text="Configuración de Alerta", bg='#f0f0f0', padx=10, pady=10)
        umbral_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        tk.Label(umbral_frame, text="Umbral de temperatura:", bg='#f0f0f0').grid(row=0, column=0)
        self.entry_umbral = tk.Entry(umbral_frame, width=10)
        self.entry_umbral.grid(row=0, column=1, padx=(10, 5))
        self.entry_umbral.insert(0, "30")  
        
        btn_config = tk.Button(umbral_frame, text="Establecer", command=self.establecer_umbral)
        btn_config.grid(row=0, column=2, padx=(5, 10))
        
        
        self.lbl_estado = tk.Label(umbral_frame, text="Estado: Normal", bg='#f0f0f0', fg='green')
        self.lbl_estado.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        
        hist_frame = tk.LabelFrame(main_frame, text="Últimas Lecturas", bg='#f0f0f0', padx=10, pady=10)
        hist_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')
        
        self.txt_historial = tk.Text(hist_frame, height=5, width=50, state='disabled')
        self.txt_historial.pack(fill=tk.BOTH, expand=True)
        
        n
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
    
    def actualizar_datos(self):
        
        self.lbl_temp.config(text=f"{self.sensor.temperatura} °C")
        self.lbl_hum.config(text=f"{self.sensor.humedad} %")
        
        
        if self.sensor.temperatura > self.sensor.umbral_alerta:
            self.lbl_estado.config(text="Estado: ALERTA - Temperatura alta", fg='red')
        else:
            self.lbl_estado.config(text="Estado: Normal", fg='green')
        
        
        self.actualizar_historial()
        
        
        self.root.after(1000, self.actualizar_datos)
    
    def actualizar_historial(self):
        self.txt_historial.config(state='normal')
        self.txt_historial.delete(1.0, tk.END)
        
        
        for registro in self.sensor.historial[-5:]:
            alerta = "ALERTA" if registro['alerta'] else "Normal"
            linea = f"{registro['timestamp']} - Temp: {registro['temperatura']}°C, Hum: {registro['humedad']}% - {alerta}\n"
            self.txt_historial.insert(tk.END, linea)
        
        self.txt_historial.config(state='disabled')
        self.txt_historial.see(tk.END)  
    
    def establecer_umbral(self):
        try:
            valor = self.entry_umbral.get()
            if self.sensor.set_umbral(valor):
                messagebox.showinfo("Éxito", f"Umbral establecido a {valor}°C")
            else:
                raise ValueError("Valor no numérico")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido")
    
    def cerrar_aplicacion(self):
        self.sensor.detener_lecturas()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()