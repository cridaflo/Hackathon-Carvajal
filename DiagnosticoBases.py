import numpy as np 
import pandas as pd 
from scipy.stats import pearsonr


#--------------------Carga de datos------------------------
def get_frames(path):
    
    """Obtiene los dataframes del archivo.
    
        Se retorna una lista con dataframes donde se encuentra la informacion
        contenida en el archivo recibido. El archivo puede ser tanto .xslx como
        .csv
        
    
    Parámetros:
    path -- ruta del archivo donde se almacenan los datos
    """
    rta = []
    extensiones = path.split('.')
    if extensiones[-1]=='xlsx':
        excel = pd.ExcelFile(path)
        hojas = excel.sheet_names
        for nombre in hojas:
            temp = excel.parse(nombre)
            rta.append(temp)
    elif extensiones[-1]=='csv':
        rta.append(pd.read_csv(path))
    return rta



#-----------metodos relacionados con entradas nan---------

def null_count(df):
    """Cuenta la cantidad de entradas nulas en el dataframe
   
    Parámetros:
    df -- data frame utilizado
    """
    temp = df.isnull()
    return temp.sum().sum()

def null_percentage(df):
    """Calcula el porcentaje de entradas nulas en el dataframe
   
    Parámetros:
    df -- data frame utilizado
    """
    dims = df.shape
    tam = dims[1]*dims[0]
    return (null_count(df)/tam)*100.0

def detect_null_rows(df):
    """Obtiene los indices de las filas que tienen todas sus entradas nulas
   
    Parámetros:
    df -- data frame utilizado
    """
    dims = df.shape
    n_filas = dims[0]
    rta = []
    for i in range(n_filas):
        fila = df.loc[i]
        if fila.isnull().sum()==dims[1]:
            rta.append(i)
    return rta
                    
def percentage_null_rows(df):
    """Calcula el porcentaje de filas nulas en el dataframe
   
    Parámetros:
    df -- data frame utilizado
    """
    filas = detect_null_rows(df)
    dims = df.shape
    return len(filas)/dims[0]

def remove_rows_with_null(df):
    """Remueve las filas que tienen al menos una entrada nula
   
    Parámetros:
    df -- data frame utilizado
    """
    dims = df.shape
    n_filas = dims[0]
    rta = []
    for i in range(n_filas):
        fila = df.loc[i]
        if fila.isnull().sum()==0:
            rta.append(i)
    return df.loc[rta,:]



def empty_column(col):
    """revisa si una columna esta vacia o no
   
    Parámetros:
    col -- columna a revisar
    """
    return col.isnull().sum()==col.shape[0]

def empty_columns(df):
    """Obtiene las columnas que tienen todas sus entradas nulas
   
    Parámetros:
    df -- data frame utilizado
    """
    rta =[]
    columnas = df.columns
    for c in columnas:
        if empty_column(df.get(c)):
            rta.append(c)
    return rta

#----------revision de id-----------------------

def count_elements_columns(df):
    
    columnas = df.columns
    tams = []
    for c in columnas:
        conj = set()
        for d in df[c]:
            if not pd.isna(d):
                conj.add(d)
        #print(conj)
        tams.append(len(conj))
    return tams


def check_unique(col):
    """Revisa si todas las entradas de una columna son diferentes
        
        No se tienen en cuenta las entradas que son nulas
   
    Parámetros:
    col -- columna revisada
    """
    conj = set()
    for d in col:
        if not pd.isna(d):
            conj.add(d)

    nulos = col.isnull().sum()
    return len(conj) == col.shape[0]-nulos and len(conj)>0


def check_id(df):
    """Revisa si en el dataframe hay una columna que pueda utilizarase como id
   
    Parámetros:
    df -- data frame revisado
    """
    columnas = df.columns
    for c in columnas:
        if(check_unique(df.get(c))):
            return True
    return False


#-------busca filas repetidas--------------------------------


def equal_rows(r1, r2, nombre):
    """Revisa si dos columnas son iguales, es decir, si los valores en todas sus entradas son los mismos
   
    Parámetros:
    r1, r2 -- filas a comparar
    """
    #print('--------------------')
    #print(r1)
    #print(r2)
    
    for i in range(r1.shape[0]-1):
        if not r1[i]==r2[i]:
            if not (pd.isna(r1[i]) and pd.isna(r2[i])):
                return False
    return True

def repeated_rows(df):
    """Obtiene los indices de filas repetidas en el dataframe
   
    Parámetros:
    df -- data frame revisado
    """

    tams = count_elements_columns(df)
    columnas = df.columns
    n_filas = df.shape[0]
    best_index = 0
    best_count = 0
    
    for i in range(len(tams)):
        t = tams[i]
        if(t>best_count):
            best_count = t
            best_index = i
        

    df2 = df.copy()
    nombre = 'indices'
    k = 0
   
    while nombre in columnas:
        nombre = 'indices%d'%(k)

    
    df2[nombre]=list(range(0,n_filas))
    df2 = df2.sort_values(list(columnas), kind='quicksort')
    rta = []
    conj_actual = []
    fila_actual = df2.iloc[0]
    n_filas= df.shape[0]
    

    for i in range(1,n_filas):
        fila = df2.iloc[i]
        if fila[best_index] != fila_actual[best_index]:
            if len(conj_actual) >0:
                rta.append(conj_actual)
                conj_actual = []
        else:

            if equal_rows(fila,fila_actual, nombre):
                if(len(conj_actual)==0):
                    conj_actual.append(fila_actual[nombre])
                conj_actual.append(fila[nombre])
            else:
                if len(conj_actual) >0:
                    rta.append(conj_actual)
                    conj_actual = [] 
        fila_actual = fila
    return rta


#------funciones asociada con los tpos de datos en columnas----------------------
def check_number_string(col):
    """Calcula la cantidad de entradas con datos de tipo string, numeríco y nulos en una columna
   
    Parámetros:
    col -- columna revisada
    """
    number = 0
    string = 0
    nan = 0
    for d in col:
        try:
            f =float(d)
            if np.isnan(f):
                nan +=1
            else:
                number +=1
        except:
            string+=1
    return number, string, nan


def check_type_columns(df):
    """Obtiene las columnas en las que los datos son pueramente numéricos, en las que son unicamente strings
        y en las que hay de ambos tipos de datos
    
    Parámetros:
    df -- data frame revisado
    """
    numbers = []
    strings = []
    mixed = []
    columnas = df.columns
    
    for c in columnas:
        #print(c)
        number, string, nan = check_number_string(df.loc[:,c])
        if number>0 and string > 0:
            mixed.append(c)
        elif number >0:
            numbers.append(c)
        elif string>0:
            strings.append(c)
    #print(numbers)
    #print(strings)
    #print(mixed)
    return numbers, strings, mixed

#-------busqueda de relaciones lineales entre columnas---------------------

def linear_correlation(df):
    """Busca relaciones lineales entre columnas del dataframe.   
        Retorna parejas de columnas que presenten un relación lineal entre ellas, es decir,se
        cumple la siguiente relación para toda fila i.
        
        y_i = m*x_i+b
        
        donde y_i es el dato de la primera columna y x:i el de la segunda.
        Para relizar el análisis se remueven las filas donde alguna de la columnas sea nula.        
        
        
    Parámetros:
    df -- data frame revisado
    """
    rta = []
    columnas = check_type_columns(df)[0]
    df = df.loc[:, columnas]
    #print(columnas)
    #print('columas: %d'%(len(columnas)))
    for i in range(len(columnas)):
        #print('i = %d'%(i))
        for j in range (i+1, len(columnas)):
            cols = df.get([columnas[i], columnas[j]])
            cols = remove_rows_with_null(cols)
            n_filas= cols.shape[0]
            s1 = cols.iloc[:,0].tolist()
            s2 = cols.iloc[:,1].tolist()
            c1 = len(s1)
            if c1>0:
                corr, p_value = pearsonr(s1, s2)
                if corr>0.99:
                    rta.append([columnas[i], columnas[j]])
    return rta

#------------Diagnostico------------------------------------------

def diagnosticar(path):
    frames = get_frames(path)
    rta = ''
    textos = []
    i = 1
    for df in frames:
        #rta+=('Diagnóstico hoja %d :\n\n'%(i))

        #---------------se revisan celdas vacias-------------------------------
        nullc = null_count(df)
        nullp = null_percentage(df)
        #rta+=('Hay prsentes %d celdas vacías, esto corresponde al %.2f porciento de su base de datos\n\n'%(nullc, nullp))
        textos.append('Hay presentes %d celdas vacías, esto corresponde al %.2f porciento de su base de datos\n'%(nullc, nullp))
        #print(1)
        #---------------se revisan filas vacias---------------------------------
        nullrc = detect_null_rows(df)
        nullrp = percentage_null_rows(df)
        if len(nullrc) == 0:
            #rta+='No hay ninguna fila vacía\n'
            textos.append('No hay ninguna fila vacía\n')
        else:
            #rta+=('Hay prsentes %d filas vacías, esto corresponde al %.2f porciento de las filas en su base de datos\n'%(len(nullrc), nullrp))
            textos.append('Hay presentes %d filas vacías, esto corresponde al %.2f porciento de las filas en su base de datos\n'%(len(nullrc), nullrp))
            #rta+='Las filas vacias son las siguientes:\n'
            temp = 'Las filas vacías son las siguientes:'
            for n in nullrc:
                #rta+='%d\n'%(n+2)
                temp+='%d,'%(n+2)
            textos.append(temp[:-1])
        #rta+='\n'
        #print(2)
        #-------------Se revisan columnas vacias-------------------------
        nullcc = empty_columns(df)

        if len(nullcc)==0:
            #rta+='No hay ninguna columna vacía\n'
            textos.append('No hay ninguna columna vacía\n')
        else:
            #rta+=('Hay prsentes %d columnas vacías\n'%(len(nullcc)))
            textos.append('Hay presentes %d columnas vacías\n'%(len(nullcc)))
            #rta+='Las columnas vacias son las siguientes:\n'
            temp = 'Las columnas vacías son las siguientes:'
            for c in nullcc:
                #rta+=c+'\n'
                temp+=c+','
            textos.append(temp)
        #rta+='\n'
        #print(3)
        #-----------Se revisa la existencia de alguna columna id------------------------
        id = check_id(df)
        if not id:
            #rta+='No hay ninguna columna con valores únicos que pueda utilizarse como id\n\n'
            textos.append('No hay ninguna columna con valores únicos que pueda utilizarse como id\n')

        #print(4)
        #------------------se revisan filas repetidas-----------------------------
        frep = repeated_rows(df)
        if len(frep)==0:
            #rta+='No hay filas repetidas\n'
            textos.append('No hay filas repetidas\n')
        else:
            #rta+='Hay %d filas repetidas\n'%(len(frep))
            textos.append('Hay %d conjuntos de filas repetidas\n'%(len(frep)))
            #rta+='Las parejas de filas repetidas son las siguientes:\n'
            temp = 'Los conjuntos de filas repetidas son los siguientes:'
            for conj in frep:
                #rta+='%d y %d\n'%(p[0]+2, p[1]+2)
                empezo = False
                for x in conj:
                    if empezo:
                        temp+=','
                    empezo = True
                    temp+='%d'%(x+2)
                temp+=';'

            textos.append(temp[:-1])
        #rta+='\n'
        #print(5)
        #---------------- se revisan columnas con datos mixtos--------------------
        mixed = check_type_columns(df)[2]
        if(len(mixed)>0):
            #print(mixed)
            #rta+='Hay %d columnas con datos que son tanto numéricos como cadenas de caracteres repetidas\n'%(len(mixed))
            textos.append('Hay %d columnas con datos que son numéricos y otros cadenas de caracteres\n'%(len(mixed)))
            #rta+='Las siguientes columnas son:\n'
            temp = 'Las columnas son:'
            for p in mixed:
                #rta+=p[0]+'\n'
                temp += p+','
            textos.append(temp[:-1])
            #rta+='\n'
        #print(6)
        #--------------- se buscan relaciones lineales----------------------------
        #corr = linear_correlation(df)
        #if(len(corr)>0):
            #rta+='Hay %d parejas de columnas que presentan una correlación lineal fuerte\n'%(len(corr))
            #textos.append('Hay %d parejas de columnas que presentan una correlación lineal fuerte\n'%(len(corr)))
            #rta+='Las parejas de columnas son las siguientes:\n'
            #temp = 'Las parejas de columnas son las siguientes:\n'
            #for p in corr:
                #rta+=p[0]+' y '+p[1]+'\n'
                #temp += p[0]+' y '+p[1]+';'
            #textos.append(temp)
            #rta+='\n'
        
        #rta+='\n\n\n'
        #print(7)
        #----------------------se retorna--------------------------------------
        i +=1
        
        #for t in textos:
            #print (t)
        print(textos)

        json = {'Estado':'Excel','texto':textos,'numCeldasVacias': str(nullc), 'porCeldasVacias': str(nullp), 'numFilasVacias':str(len(nullrc)), 
        'porFilasVacias':str(nullrp), 'numColVacias':str(len(nullcc)), 'id': id, 'numFilasRepetidas':str(len(frep)),  
        'numDatosMixtos': str(len(mixed))}
        
    
        
        return json
        



        
    

#---------pruebas de buen funcionamiento------------------------ 


