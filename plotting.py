import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
import pandas as pd
import os

# --- REGISTRO DIRECTO DE FUENTES ---
font_files = ["BOOKOS.TTF", "BOOKOSB.TTF", "BOOKOSI.TTF", "BOOKOSBI.TTF", "BookmanOldStyle.ttf"]
custom_font_name = 'serif' 

for font_file in font_files:
    if os.path.exists(font_file):
        try:
            font_manager.fontManager.addfont(font_file)
            prop = font_manager.FontProperties(fname=font_file)
            custom_font_name = prop.get_name()
        except Exception:
            pass

def create_chart(df, parameter, selected_columns=None, date_angle=-90, date_format="MM-YY", x_label_count=0, legend_position="right", symbol_style="circle", legend_size=7.0, legend_cols=5, symbol_size=3.0, legend_spacing=0.2):
    
    subset = df[df['parametro'] == parameter].copy()
    if subset.empty:
        return None
    
    subset['fecha'] = pd.to_datetime(subset['fecha'])
    unit = subset['unidad'].iloc[0] if 'unidad' in subset.columns else ""
    
    # --- CONFIGURACIÓN GLOBAL ---
    plt.rcParams['font.family'] = custom_font_name
    if custom_font_name == 'serif':
        plt.rcParams['font.serif'] = ['Bookman Old Style', 'Times New Roman', 'serif']
        
    plt.rcParams['font.size'] = 9
    plt.rcParams['mathtext.default'] = 'regular' 
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['axes.spines.top'] = True
    plt.rcParams['axes.spines.right'] = True
    plt.rcParams['axes.spines.bottom'] = True
    plt.rcParams['axes.spines.left'] = True
    
    fig, ax = plt.subplots(figsize=(15.5 / 2.54, 8 / 2.54))
    
    # --- MARCADORES ---
    marker_configs = [('o', True), ('s', True), ('D', True), ('^', True), ('p', True), ('h', True), ('*', True), ('v', True), ('<', True), ('>', True), ('X', True), ('d', True), ('P', True), ('H', True), ('8', True), ('o', False), ('s', False), ('D', False), ('^', False), ('p', False), ('h', False), ('*', False), ('v', False), ('<', False), ('>', False), ('X', False), ('d', False), ('P', False), ('H', False), ('8', False), ('+', True), ('x', True), ('|', True), ('_', True), ('1', True), ('2', True), ('3', True), ('4', True)]
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#7fff00', '#fabed4', '#469990', '#dcbeff', '#9a6324', '#4b0082', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#333333', '#ffd700', '#ff7f50', '#87ceeb', '#a87858', '#ff69b4', '#dda0dd', '#40e0d0', '#d2691e', '#4682b4', '#7fff00', '#4b0082', '#04bbfc']
    
    # --- GRAFICAR ---
    stations = subset['estacion'].unique()
    for i, station in enumerate(stations):
        station_data = subset[subset['estacion'] == station]
        c = colors[i % len(colors)]
        if symbol_style == "varied":
            m_shape, is_filled = marker_configs[i % len(marker_configs)]
            mfc = c if is_filled else 'none'
            ax.plot(station_data['fecha'], station_data.get('valor_num', station_data['valor']), marker=m_shape, linestyle='', color=c, markerfacecolor=mfc, markeredgecolor=c, label=station, markersize=symbol_size)
        else:
            ax.plot(station_data['fecha'], station_data.get('valor_num', station_data['valor']), marker='o', linestyle='', color=c, markerfacecolor=c, markeredgecolor=c, label=station, markersize=symbol_size)

    # --- NORMAS Y EJES ---
    limit_cols = [col for col in df.columns if col.startswith(('lim_', 'ISQG', 'PEL'))]
    if selected_columns:
        limit_cols = [col for col in limit_cols if col in selected_columns]

    for col in limit_cols:
        val = subset[col].iloc[0]
        if pd.notna(val):
            ax.axhline(y=val, color='black', linestyle='--', alpha=0.5, label=col, linewidth=1)

    # --- SUBÍNDICES Y FORMATO CIENTÍFICO ---
    # Convertimos los nombres de parámetros químicos y el nombre científico
    display_p = parameter.replace("NO3", "NO$_3$").replace("NO2", "NO$_2$").replace("DBO5", "DBO$_5$").replace("Escherichia coli", "$\mathit{\mathbf{Escherichia\ coli}}$")
    
    ax.set_ylabel(f"{display_p} ({unit})", fontweight='bold', fontsize=9)
    
    def y_fmt(x, pos): return f"{x:g}".replace('.', ',')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(y_fmt))
    
    ax.grid(True, which='both', axis='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # --- FECHAS ---
    def span_date_fmt(x, pos):
        dt = mdates.num2date(x)
        return f"{dt.day}-{['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][dt.month-1]}-{str(dt.year)[-2:]}" if date_format == "DD-MM-YY" else f"{['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'][dt.month-1]}-{str(dt.year)[-2:]}"
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(span_date_fmt))
    ax.xaxis.set_major_locator(plt.MaxNLocator(x_label_count) if x_label_count > 0 else plt.MaxNLocator(8))
    plt.xticks(rotation=date_angle)
    
    # --- LEYENDA ---
    if legend_position == "bottom":
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=legend_cols, fontsize=legend_size, frameon=False, labelspacing=legend_spacing)
    else:
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), ncol=1, fontsize=legend_size, frameon=False, labelspacing=legend_spacing)
                  
    plt.tight_layout()
    return fig