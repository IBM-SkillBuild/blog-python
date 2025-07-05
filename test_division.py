def dividir_texto(texto, longitud_aproximada=3000):
    """
    Divide el texto en trozos de longitud aproximada, respetando los puntos.
    """
    if not texto or len(texto.strip()) == 0:
        return []
    
    texto = texto.strip()
    trozos = []
    inicio = 0
    
    while inicio < len(texto):
        fin = min(inicio + longitud_aproximada, len(texto))
        
        if fin < len(texto):
            # Buscar el último punto dentro del rango
            ultimo_punto = texto.rfind('.', inicio, fin)
            
            if ultimo_punto != -1:
                fin = ultimo_punto + 1  # Incluir el punto
            else:
                # Si no hay punto, buscar el siguiente
                siguiente_punto = texto.find('.', fin)
                if siguiente_punto != -1:
                    fin = siguiente_punto + 1
                else:
                    # Si no hay puntos, buscar el último espacio
                    ultimo_espacio = texto.rfind(' ', inicio, fin)
                    if ultimo_espacio != -1:
                        fin = ultimo_espacio + 1
        
        trozo = texto[inicio:fin].strip()
        if trozo:  # Solo agregar trozos no vacíos
            trozos.append(trozo)
        
        inicio = fin
        
        # Prevenir bucle infinito
        if inicio >= len(texto):
            break
    
    # Si no se pudo dividir, devolver el texto completo
    if not trozos:
        trozos = [texto]
    
    print(f"Texto dividido en {len(trozos)} trozos:")
    for i, trozo in enumerate(trozos, 1):
        print(f"  Trozo {i}: {len(trozo)} caracteres")
    
    return trozos

# Texto de prueba más largo
texto_prueba = "Este es un texto muy largo que debería ser dividido en múltiples trozos. La función de división respeta los puntos y espacios para evitar cortar frases a la mitad. Esto es importante para mantener la coherencia del audio generado. El sistema está diseñado para manejar textos de hasta 10,000 caracteres de manera eficiente. Cada trozo se procesa por separado y luego se concatenan todos los archivos de audio en uno solo. Esto permite generar audios de alta calidad incluso con textos muy largos. La limpieza automática de archivos temporales asegura que el servidor no se llene de archivos innecesarios. El sistema también incluye manejo robusto de errores y logging detallado para facilitar el debugging. Todo esto hace que la generación de audio sea confiable y eficiente. Ahora voy a añadir más contenido para asegurar que el texto sea lo suficientemente largo como para ser dividido. La división se realiza aproximadamente cada 3000 caracteres, respetando los puntos y espacios. Esto es crucial para mantener la naturalidad del audio generado. El sistema de concatenación utiliza moviepy para combinar todos los archivos de audio en uno solo. La gestión de memoria es importante para evitar problemas con archivos grandes. Los archivos temporales se eliminan automáticamente después de la concatenación. El sistema también incluye validaciones para asegurar que los archivos se generen correctamente. Todo el proceso está optimizado para ser eficiente y confiable. Voy a continuar añadiendo más texto para asegurar que supere los 3000 caracteres. La API de Speechify tiene limitaciones en la longitud de texto que puede procesar en una sola llamada. Por eso es importante dividir textos largos en trozos manejables. Cada trozo se procesa independientemente y luego se combinan todos los resultados. Esto permite manejar textos de cualquier longitud de manera eficiente. El sistema también incluye manejo de errores para casos donde algún trozo falle en la generación. La limpieza automática de archivos temporales es crucial para mantener el servidor funcionando correctamente. Los archivos antiguos se eliminan automáticamente después de una hora para evitar llenar el disco duro. El sistema está diseñado para ser robusto y confiable en producción. La gestión de memoria es importante para evitar problemas con archivos grandes. Los clips de audio se cargan en memoria para la concatenación y se liberan después del uso. Esto asegura que el sistema no consuma demasiada memoria. El logging detallado permite monitorear el proceso y detectar problemas rápidamente. Todo el sistema está optimizado para funcionar de manera eficiente y confiable. Voy a añadir aún más texto para asegurar que definitivamente supere los 3000 caracteres y active la división automática del texto en múltiples trozos para su procesamiento individual. Ahora voy a añadir más contenido para asegurar que el texto sea definitivamente más largo que 3000 caracteres. Esto es importante para probar la funcionalidad de división de texto. La función dividir_texto está configurada para dividir en trozos de aproximadamente 3000 caracteres. Cuando el texto supera esta longitud, el sistema debería dividirlo automáticamente en múltiples trozos. Cada trozo se procesa por separado usando la API de Speechify. Luego todos los archivos de audio generados se concatenan en uno solo usando moviepy. Esto permite manejar textos de cualquier longitud de manera eficiente. El sistema también incluye limpieza automática de archivos temporales para evitar llenar el servidor. Los archivos antiguos se eliminan después de una hora para mantener el espacio en disco. Todo el proceso está optimizado para ser robusto y confiable. La gestión de memoria es importante para evitar problemas con archivos grandes. Los clips de audio se cargan en memoria para la concatenación y se liberan después del uso. El logging detallado permite monitorear el proceso y detectar problemas rápidamente. El sistema está diseñado para funcionar de manera eficiente en producción."

print(f"Longitud del texto de prueba: {len(texto_prueba)} caracteres")
trozos = dividir_texto(texto_prueba)
print(f"Resultado: {len(trozos)} trozos generados") 