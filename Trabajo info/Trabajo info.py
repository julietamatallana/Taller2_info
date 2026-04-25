import pandas as pd
import scipy.io
import matplotlib.pyplot as plt

#PARTE 1 DE TALLER
#traer datos csv de clinical_data
dataf_clinical = pd.read_csv('clinical_data.csv')
#Extraer datos de dataf_clinical
print(dataf_clinical)
#Verificar su estructura (dimensiones, tipos de datos y valores faltantes)
forma=dataf_clinical.shape
print(forma)
tipos_datos=dataf_clinical.dtypes
print(tipos_datos)
valores_faltantes=dataf_clinical.isnull().sum() 
#Si la celda está vacía osea NaN, le pone un True, sino le pone un False y sumas los true
print(valores_faltantes)

# Calcular estadisticas descriptivas basicas 
var_num=['Edad','Frecuencia_Cardiaca','PAM','Glucosa']
media=dataf_clinical[var_num].mean()
print(media)
desviacion = dataf_clinical[var_num].std()
print(desviacion)
minimo = dataf_clinical[var_num].min()
print(minimo)
maximo = dataf_clinical [var_num].max()
print(maximo)

#Grafica exploratoria
datos_glucosa=dataf_clinical.iloc[:,6]
plt.subplot(1,2,1)
plt.violinplot(datos_glucosa)
plt.title('Glucosa1')
plt.subplot(1,2,2)
plt.hist(dataf_clinical['Frecuencia_Cardiaca'])
plt.title('Frecuencia Cardiaca2')
plt.show()


