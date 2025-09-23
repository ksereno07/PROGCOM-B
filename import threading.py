import ast
import sys
import traceback
import re

def revisar_codigo(codigo):
    print("analizando tu codigo...")
    print()
    
    # revisar sintaxis primero
    try:
        ast.parse(codigo)
        print("✓ sintaxis correcta")
    except SyntaxError as error:
        print("❌ ERROR DE SINTAXIS:")
        print(f"   linea {error.lineno}: {error.msg}")
        
        # mostrar la linea exacta
        lineas = codigo.split('\n')
        if error.lineno <= len(lineas):
            linea_mala = lineas[error.lineno-1]
            print(f"   codigo: {linea_mala.strip()}")
            
            # dar solucion especifica
            if "invalid syntax" in str(error.msg):
                if re.search(r'\b(if|elif|else|for|while|def|class)\b.*[^:]$', linea_mala.strip()):
                    print(f"   SOLUCION: agrega ':' al final → {linea_mala.strip()}:")
                elif linea_mala.count('(') > linea_mala.count(')'):
                    print("   SOLUCION: cierra el parentesis → agrega ')'")
                elif linea_mala.count('[') > linea_mala.count(']'):
                    print("   SOLUCION: cierra el corchete → agrega ']'")
                elif linea_mala.count('{') > linea_mala.count('}'):
                    print("   SOLUCION: cierra la llave → agrega '}'")
                elif linea_mala.count('"') % 2 != 0:
                    print("   SOLUCION: cierra las comillas → agrega '\"'")
                elif linea_mala.count("'") % 2 != 0:
                    print("   SOLUCION: cierra las comillas → agrega \"'\"")
                else:
                    print("   SOLUCION: revisa la escritura de esa linea")
            elif "indentation" in str(error.msg).lower():
                print("   SOLUCION: usa 4 espacios para indentar (no tabs)")
            elif "unexpected indent" in str(error.msg).lower():
                print("   SOLUCION: quita espacios de mas al inicio de la linea")
        print()
        return
    
    # ejecutar para encontrar errores
    print("✓ ejecutando codigo...")
    
    try:
        # crear namespace vacio para evitar conflictos
        namespace = {}
        exec(codigo, namespace)
        print("✓ el codigo funciona bien!")
        
    except Exception as error:
        print("❌ ERROR DE EJECUCION:")
        
        # encontrar linea exacta del error
        tb_list = traceback.extract_tb(error.__traceback__)
        linea_error = None
        
        for frame in tb_list:
            if frame.filename == '<string>' or frame.filename == '<stdin>':
                linea_error = frame.lineno
                break
        
        # mostrar la linea problematica
        lineas = codigo.split('\n')
        if linea_error and linea_error <= len(lineas):
            linea_problema = lineas[linea_error-1]
            print(f"   linea {linea_error}: {linea_problema.strip()}")
        else:
            print(f"   linea {linea_error or 'desconocida'}")
        
        print(f"   error: {type(error).__name__}: {error}")
        
        # dar solucion especifica segun el tipo de error
        if isinstance(error, NameError):
            # extraer el nombre de la variable
            match = re.search(r"name '(\w+)' is not defined", str(error))
            if match:
                var_name = match.group(1)
                print(f"   PROBLEMA: la variable '{var_name}' no existe")
                print(f"   SOLUCION: agrega esta linea antes: {var_name} = valor_que_quieras")
            else:
                print("   PROBLEMA: usas una variable que no has creado")
                print("   SOLUCION: crea la variable antes de usarla")
                
        elif isinstance(error, IndexError):
            print("   PROBLEMA: el indice esta fuera del rango de la lista")
            if linea_error and linea_error <= len(lineas):
                linea = lineas[linea_error-1]
                # buscar el indice usado
                match = re.search(r'\[(\d+)\]', linea)
                if match:
                    indice = match.group(1)
                    print(f"   SOLUCION: el indice {indice} es muy grande, usa un numero menor")
                else:
                    print("   SOLUCION: verifica que el indice sea menor a len(tu_lista)")
            
        elif isinstance(error, KeyError):
            clave = str(error).strip("'\"")
            print(f"   PROBLEMA: la clave '{clave}' no existe en el diccionario")
            print(f"   SOLUCION: agrega la clave → diccionario['{clave}'] = valor")
            print(f"   O usa → diccionario.get('{clave}', 'valor por defecto')")
            
        elif isinstance(error, ZeroDivisionError):
            print("   PROBLEMA: estas dividiendo por cero")
            if linea_error and linea_error <= len(lineas):
                linea = lineas[linea_error-1]
                print(f"   SOLUCION: cambia '{linea.strip()}' por:")
                print("   if denominador != 0:")
                print("       resultado = numerador / denominador")
                print("   else:")
                print("       print('No se puede dividir por cero')")
                
        elif isinstance(error, TypeError):
            msg = str(error).lower()
            if "unsupported operand" in msg:
                print("   PROBLEMA: estas mezclando tipos incompatibles")
                print("   SOLUCION: convierte al mismo tipo → int(), str(), float()")
            elif "not subscriptable" in msg:
                print("   PROBLEMA: ese tipo de dato no usa []")
                print("   SOLUCION: verifica que sea una lista o diccionario")
            else:
                print("   PROBLEMA: tipo de dato incorrecto")
                print("   SOLUCION: verifica los tipos de tus variables")
                
        elif isinstance(error, ValueError):
            msg = str(error).lower()
            if "invalid literal" in msg:
                print("   PROBLEMA: no se puede convertir ese texto a numero")
                print("   SOLUCION: usa try/except o verifica que sea un numero")
                print("   try:")
                print("       numero = int(texto)")
                print("   except ValueError:")
                print("       print('No es un numero valido')")
            else:
                print("   PROBLEMA: valor invalido para la operacion")
                print("   SOLUCION: verifica que el valor tenga el formato correcto")
        
        elif isinstance(error, AttributeError):
            print("   PROBLEMA: ese objeto no tiene ese metodo o atributo") 
            if "list" in str(error) and "append" not in str(error):
                print("   SOLUCION: las listas usan .append(), .remove(), .pop()")
            elif "str" in str(error):
                print("   SOLUCION: los strings usan .upper(), .lower(), .split()")
            else:
                print("   SOLUCION: verifica que el metodo exista para ese tipo de dato")
        
        elif isinstance(error, IndentationError):
            print("   PROBLEMA: indentacion incorrecta")
            print("   SOLUCION: usa exactamente 4 espacios para cada nivel")
            
        else:
            print("   SOLUCION: revisa la documentacion del error o busca en google")
        
        print()
    
    # revisar problemas comunes adicionales
    print("revisando otros problemas...")
    
    lineas = codigo.split('\n')
    advertencias = 0
    
    for i, linea in enumerate(lineas, 1):
        # eval peligroso
        if 'eval(' in linea:
            print(f"⚠️  linea {i}: eval() es muy peligroso")
            print("   SOLUCION: usa ast.literal_eval() o evita eval()")
            advertencias += 1
        
        # input sin conversion
        if 'input(' in linea and not any(conv in linea for conv in ['int(', 'float(', 'str(']):
            if '=' in linea:
                var_name = linea.split('=')[0].strip()
                print(f"⚠️  linea {i}: input() siempre da texto")
                print(f"   SOLUCION: usa {var_name} = int(input('...')) para numeros")
                advertencias += 1
        
        # range con len innecesario
        if 'for' in linea and 'range(len(' in linea:
            print(f"⚠️  linea {i}: usar range(len()) es ineficiente")
            print("   SOLUCION: usa 'for item in lista:' directamente")
            advertencias += 1
    
    if advertencias == 0:
        print("✓ no hay otros problemas evidentes")
    
    print()
    print("analisis terminado!")

# programa principal
print("=== ANALIZADOR DE CODIGO ===")
print("pega tu codigo python y te dire exactamente que esta mal")
print("(presiona Enter dos veces para terminar)")
print()

lineas_codigo = []
lineas_vacias = 0

while True:
    try:
        linea = input()
        if linea.strip() == "":
            lineas_vacias += 1
            if lineas_vacias >= 2:
                break
        else:
            lineas_vacias = 0
            lineas_codigo.append(linea)
    except (EOFError, KeyboardInterrupt):
        break

if lineas_codigo:
    codigo_completo = '\n'.join(lineas_codigo)
    print()
    print("="*50)
    revisar_codigo(codigo_completo)
else:
    print("no recibí codigo para revisar")