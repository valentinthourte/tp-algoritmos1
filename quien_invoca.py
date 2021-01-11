def archivo_analizador(texto):
    """[Autor: Alfonso]
    [Ayuda: recibe un string como parametro y escribe en el archivo analizador.txt]
    """
    with open ("analizador.txt","a") as archivo_generado:
        archivo_generado.write(texto)
    
def quien_invoca_a_quien():
    """[Autor: Alfonso]
       [Ayuda: Genera un diccionario de quien inoca a quien, 
       teniendo como clave el nombre de la funcion y como valores una lista de lista con cuantas veces lo invoca, 
       ademas devuelve los nombres de todas las funciones del programa]
    """
    import modulo_csv
    fuente = 'fuente_unico.csv'
    #Invoco para leer el csv y que me devuelva un diccionario
    diccionario_csv = modulo_csv.leer_csv(fuente)
    #Declaro variables
    nombre_funcion = []
    resultado = {}
    for fila in diccionario_csv:
        nombre_funcion.append(fila)
    #Recorre las filas del diccionario y me quedo con la clave (nombre_funcion) y el cuerpo de la funcion
    for fila in diccionario_csv.items():
        clave = fila[0]
        cuerpo = fila[1][2:]
        #Por cada funcion en la lista de  todas las funciones itera
        for funcion in nombre_funcion:
            #Cheque si en el cuerpo de la funcion existe el nombre de la funcion y lo anade a la lista
            funciones_en_cuerpo = [s for s in cuerpo if funcion in s]
            contador = len(funciones_en_cuerpo)
            #Genera una lista con el nombre de la funcion invocada y cuantas veces fue invocada
            lista_de_invocacion = [funcion,contador]
            
            if contador > 0:
                if clave in resultado:
                    resultado[clave].append(lista_de_invocacion)
                else:    
                    resultado[clave] = [lista_de_invocacion]
    return nombre_funcion, resultado

def armar_tabla():
    """[Autor: Alfonso]
    [Ayuda: Genera tres listas, una con el titulo, una lista de listas con cada linea y espacio, y los totales]
    """   
    lista_funciones , dicc_datos = quien_invoca_a_quien()
    enum_datos = list(enumerate(lista_funciones,1))
    #Obtengo una lista con  el numero de cada funcion
    posicion = primer_item_lista(enum_datos)
    #Calculo la maxima cantidad de funciones y le doy formato al titulo de la tabla
    maximo,titulo = formato_titulo(posicion)

    lista_total = []   
    vacio = " "
    
    #Recorro la lista que genera el enumerate
    for numero,funcion in enum_datos:
        
        conteo = 1
        primer_campo = str(numero) + " " + funcion 
        
        #Genero la lista que voy a imprimir con el primer campo justificandola a 32 espacios
        lista_a_imprimir = [primer_campo.ljust(32)]
        
        #Lleno la tabla con vacios para formar una grilla validando contra el numero total de funciones
        while conteo <= maximo:
            lista_a_imprimir.append(vacio)
            conteo += 1
        
        for clave, valor in dicc_datos.items():
            
            for lista in valor:
                
                #Si el nombre de la funcion esta en la lista del cuerpo
                if funcion in lista:
                    
                    #Busco el numero en que fue invocada
                    numero_invocada =   [l for l in enum_datos if clave in l]
                    #Busco el nombre de la funcion invocada
                    funcion_a_invocar = numero_invocada[0][0]
                    #Le agrego una X a la funcion que invocaron
                    lista_a_imprimir[funcion_a_invocar] = 'X'
        #Reemplazo los campos vacios por las veces que fue invocada
        if funcion  in dicc_datos:
            dicc_informacion = dicc_datos[funcion]
            lista_modificar = []
            for i,j in dicc_informacion:
                
                #Calculo a cual funcion invoco basada en el numero
                numero_invocada =   [l for l in enum_datos if i in l] 
                #Busca el nombre de la funcion invocada
                funcion_a_invocar = numero_invocada[0][0]
                #Modifico la posicion en la lista con cuantas veces lo invoco
                lista_a_imprimir[funcion_a_invocar] = j
                 
        #Creo una lista de lista que contenga todo para calcular los totales en la matriz
        lista_total.append(lista_a_imprimir)        

    totales = generar_totales(lista_total)
   
    return titulo, lista_total, totales
            
def borrar_primer_indice(lista):
    """ [Autor: Alfonso]
        [Ayuda: Borra el primer indice de una lista, acepta como parametro de entrada una lista]
    """
    lista_2 = lista
    for i in lista_2:
        del i[0]          
    return lista_2

def borrar_un_valor_lista(lista,valor):
    """ [Autor: Alfonso]
        [Ayuda: Reemplaza un valor en especifico de una lista por vacio y retorna la lista modificada]
    """
    lista_valor =[list(map(lambda x: x if x!= valor else 0, i)) for i in lista]
    return lista_valor

def generar_totales(lista):
    """ [Autor: Alfonso]
        [Ayuda: Recibe una lista y genera la lista de sumatoria de totales y la devuelve]
    """
    
    vacio = ' '
    #Hago una lista de listas de los totales reemplazando los vacios por 0 para poder sumarlo
    lista_totales_numero = borrar_un_valor_lista(lista,vacio)
    lista_totales_numero_2 = borrar_un_valor_lista(lista_totales_numero, 'X')   
    borrar_primer_indice(lista_totales_numero_2)
    totales1 = sumar_totales(lista_totales_numero_2)  
    
    return totales1

def sumar_totales(lista):
    """ [Autor: Alfonso]
        [Ayuda: Toma como parametro de entrada una lista, y genera una nueva lista sumando los valores de cada columna de la lista inicial]
    """
    totales = []  
    for columna_matriz in enumerate(lista[0]):
        suma_columna = sum([x[columna_matriz[0]] for x in lista])
        totales.append(suma_columna)
    totales.insert(0,"Total Invocaciones              ")
    return totales

def formato_titulo(lista):
    """ [Autor: Alfonso]
        [Ayuda: Le da formato al titulo]
    """
    #Calculo la maxima cantidad de funciones
    maximo =max(lista)
    #Formato de Titulo
    titulo = lista
    #Hay 32
    titulo.insert(0,"Funciones                       ")
    
    return maximo,titulo
    
def la_tabla():
    """ [Autor: Alfonso]
        [Ayuda: Armado de la tabla para el analizador]
    """
    titulo, cuerpo, total = armar_tabla()
    
    #Titulo
    titulo = formato_tabla(titulo)
    print(titulo)
    titulo = titulo + "\n"
    archivo_analizador(titulo)
    
    #Cuerpo
    formato_cuerpo(cuerpo)
    
    #Total
    total = formato_tabla(correcto_espaciado(total))
    print(total)
    total = total + "\n"
    archivo_analizador(total)
    
        
def formato_tabla(lista):   
    """[Autor: Alfonso]
    [Ayuda: Le da formato de tabla a una lista con espaciado y divisiones]
    """
    str_nuevo = ' | '.join(map(str, lista))
    return str_nuevo

def formato_cuerpo(lista):
    """[Autor: Alfonso]
    [Ayuda: Le da formato a una lista para que imprima el cuerpo]
    """
    for i in lista:
        i = formato_tabla(correcto_espaciado(i))
        print(i)
        i = i + '\n'
        archivo_analizador(i)
    return i

def correcto_espaciado(lista_1):
    """[Autor: Alfonso]
    [Ayuda: Modifica el espaciado de los espacios en blanco para que quede a la par cada columna despues de la decima]
    """
    for j,k in enumerate(lista_1):
            if j >= 10 and len(str(k))<2:
               lista_1[j] = ' ' + str(k)
            elif j >= 10 and len(str(k))>=2:
                lista_1[j] = str(k)
            elif j >= 100 and len(str(k))<2:
                lista_1[j] = '  ' + str(k)
            elif j >= 100 and len(str(k))>=2:
                lista_1[j] = ' ' + str(k)    
    return lista_1

def primer_item_lista(lista): 
    """[Autor: Alfonso]
        [Ayuda: Busca el primer item de una lista, recibe una lista, y devuelve un item]
    """
    return [item[0] for item in lista] 