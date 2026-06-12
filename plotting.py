# 3. Formato de Ejes
    # --- CONVERSIÓN DE SUBÍNDICES QUÍMICOS (Motor Matemático) ---
    # Usamos $_$ para que el motor matemático aplique el formato, 
    # y 'regular' para que use la fuente Bookman Old Style.
    
    display_parameter = parameter
    if "NO3" in parameter:
        display_parameter = parameter.replace("NO3", "NO$_3$")
    elif "NO2" in parameter:
        # Si tienes el superíndice negativo en tus datos, también lo manejará
        display_parameter = parameter.replace("NO2", "NO$_2$")
    
    ax.set_ylabel(f"{display_parameter} ({unit})", fontweight='bold', fontsize=9)