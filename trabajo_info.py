import pandas as pd
import scipy.io as sio
import matplotlib.pyplot as plt
import scipy.signal as signal

# Grupo 3
# Estudiantes:
# - Nombre Miguel Ángel Piedrahita Sánchez
# - Nombre Danna Julieta Matallana
# Unidad 2 - Taller Evaluativo: Introducción a la computación en Bioingeniería

#PARTE 1 DE TALLER
#traer datos csv de clinical_data
dataf_clinical = pd.read_csv('clinical_data.csv')
#Verificar su estructura (dimensiones, tipos de datos y valores faltantes)
dim = dataf_clinical.ndim
forma = dataf_clinical.shape
tipos_datos = dataf_clinical.dtypes
valores_faltantes = dataf_clinical.isnull().sum() #Si la celda está vacía (NaN), le pone un True, sino le pone un False y sumas los true
print(f"Los datos tienen {dim} dimensiones")
print(f"Los datos tienen una forma de {forma})")
print(f"Los tipos de datos de cada categoría son:\n{tipos_datos}")
print(f"El número de valores faltantes en cada categoría es:\n{valores_faltantes}")
print('_'*60)

# Calcular estadisticas descriptivas basicas 
var_num=['Edad','Frecuencia_Cardiaca','PAM','Glucosa']
media=dataf_clinical[var_num].mean()
print(f'El promedio de cada categoría es\n{(round(media))}')
desviacion = dataf_clinical[var_num].std()
print(f'La desviación estándar de cada categoría es\n{round(desviacion,2)}')
minimo = dataf_clinical[var_num].min()
print(f'El valor mínimo de cada categoría es\n{minimo}')
maximo = dataf_clinical [var_num].max()
print(f'El valor máximo de cada categoría es\n{maximo}')

#Grafica exploratoria
datos_glucosa=dataf_clinical.iloc[:,6]
plt.figure(figsize=(7,4))
plt.subplot(1,2,1)
plt.violinplot(datos_glucosa)
plt.ylabel('Glucosa (mg/dL)')
plt.title('Distribución de glucosa')
plt.subplot(1,2,2)
plt.hist(dataf_clinical['Frecuencia_Cardiaca'])
plt.title('Distribución de Frecuencia Cardiaca')
plt.xlabel('Frecuencia cardíaca')
plt.ylabel('Frecuencia')
plt.subplots_adjust(wspace=0.4)
plt.show()

print('_'*60)

#PARTE 2 DE TALLER
ecg_sano = sio.loadmat('ecg_sano.mat') #Cargar los archivos de ECG
ecg_taqui = sio.loadmat('ecg_taqui.mat')

#Crear clase señal
class Signal:
    def __init__(self, label):
        self.__data = []
        self.__filtro = [] #Este atributo será en el que se harán todos los procesamientos e igual seguir teniendo acceso a los datos originales
        self.__tiempo = []
        self.label = label
        self.inicio = 0 #Los límites de la muestra que se asignarán en la función corteMuestra
        self.final = 0
        self.mean = 0
        self.std = 0
    def setData(self,señal):
        self.__data = señal['ecg']
        self.__tiempo = señal['time'][0]
    def getData(self):
        return self.__data
    def getDatafilt(self):
        return self.__filtro
    def filtroNotch(self):
        b,a = signal.iirnotch(60, 30, 500) #Se utiliza un factor de calidad Q = 30 porque es común utilizar este valor en ECG
        self.__filtro = signal.filtfilt(b,a,self.__data)
    def corteMuestra(self,canal=0,pmin=500,pmax=1000):
        self.inicio = pmin
        self.final = pmax
        self.__filtro = self.__filtro[canal,pmin:pmax] #Ajustar el tamaño de la muestra
        self.__tiempo = self.__tiempo[pmin:pmax] #Ajustar el vector tiempo para la graficación
    def calcularEstadisticas(self):
        self.mean = self.__filtro.mean()
        self.std = self.__filtro.std()
        print(f'La media de los datos de ECG {self.label} en este segmento es de {round(self.mean,2)} y la desviación estandar de {round(self.std,2)}')
    def graficarDatos(self):
        plt.figure(figsize=(10,4))
        plt.subplot(2,1,1)
        plt.plot(self.__tiempo,self.__data[0,self.inicio:self.final], label = 'Datos sin filtrar')
        plt.xlabel('Tiempo')
        plt.ylabel('Amplitud')
        plt.legend()
        plt.grid()
        plt.title(f'Señal ECG {self.label} sin filtrar')
        plt.subplot(2,1,2)
        plt.plot(self.__tiempo, self.__filtro, label = 'Datos filtrados')
        plt.xlabel('Tiempo')
        plt.ylabel('Amplitud')
        plt.legend()
        plt.grid()
        plt.title(f'Señal ECG {self.label} filtrada')
        plt.subplots_adjust(hspace=0.7)
        plt.show()
    def procesarDatos(self): #Un método para juntar todos los procesos que deben hacerse
        self.filtroNotch()
        self.corteMuestra()
        self.calcularEstadisticas()
        self.graficarDatos()

    
señal_sano = Signal('sano')
señal_sano.setData(ecg_sano)
señal_sano.procesarDatos()
señal_taqui = Signal('taquicardico')
señal_taqui.setData(ecg_taqui)
señal_taqui.procesarDatos()

print('_'*60)
print('COMPARACIÓN ENTRE SEÑALES:\n') #Mostrar de manera gráfica las diferencias estadísticas en el segmento elegido
print(f"{'Estadística':<20} {'Sano':<15} {'Taquicardia':<15} {'Diferencia':<15}")
print(f"{'Media':<20} {señal_sano.mean:<15.2f} {señal_taqui.mean:<15.2f} {abs(señal_sano.mean - señal_taqui.mean):<15.2f}")
print(f"{'Desv. Estándar':<20} {señal_sano.std:<15.2f} {señal_taqui.std:<15.2f} {abs(señal_sano.std - señal_taqui.std):<15.2f}")