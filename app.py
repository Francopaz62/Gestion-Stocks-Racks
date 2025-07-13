import streamlit as st
import pandas as pd
import os

CSV_PATH = "pallets.csv"  # Asegurate que sea el nombre correcto

# Carga los datos o crea estructura base si no existe el CSV
def cargar_datos():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH, dtype=str)
    else:
        racks = ['R1', 'R2', 'R3', 'R4', 'R5']
        filas = ['A', 'B', 'C', 'D', 'E', 'F']
        columnas = ['1', '2', '3', '4']
        datos = []
        for rack in racks:
            for fila in filas:
                for col in columnas:
                    datos.append({
                        'rack': rack,
                        'slot': f"{fila}{col}",
                        'producto': '',
                        'fecha_vto': '',
                        'cantidad': '0',
                        'fecha_produccion': '',
                        'fecha_acomodado': '',
                        'lote': ''
                    })
        df = pd.DataFrame(datos)
        df.to_csv(CSV_PATH, index=False)
    df.fillna('', inplace=True)
    df['cantidad'] = df['cantidad'].apply(lambda x: int(x) if str(x).isdigit() else 0)
    return df

# Guarda el DataFrame en el CSV
def guardar_datos(df):
    df.to_csv(CSV_PATH, index=False)

def main():
    st.title("Gestión de Stock en Racks")

    df = cargar_datos()

    racks = ['R1', 'R2', 'R3', 'R4', 'R5']
    filas = ['A', 'B', 'C', 'D', 'E', 'F']
    columnas = ['1', '2', '3', '4']

    selected_rack = st.sidebar.selectbox("Seleccionar Rack", racks)

    st.header(f"Contenido del {selected_rack}")

    df_rack = df[df['rack'] == selected_rack]

    for fila in filas:
        cols = st.columns(len(columnas))
        for i, col in enumerate(cols):
            slot_id = f"{fila}{columnas[i]}"
            fila_slot = df_rack[df_rack['slot'] == slot_id]
            if not fila_slot.empty:
                fila_slot = fila_slot.iloc[0]
                texto = f"**{slot_id}**\n"
                if fila_slot['producto']:
                    texto += f"Prod: {fila_slot['producto']}\n"
                    texto += f"Cantidad: {fila_slot['cantidad']}\n"
                    texto += f"Vto: {fila_slot['fecha_vto']}\n"
                else:
                    texto += "_Vacío_"
            else:
                texto = f"**{slot_id}**\n_Vacío_"

            if col.button(texto, key=slot_id):
                st.session_state['edit_rack'] = selected_rack
                st.session_state['edit_slot'] = slot_id

    if 'edit_slot' in st.session_state:
        slot = st.session_state['edit_slot']
        rack = st.session_state['edit_rack']
        st.subheader(f"Editar/Agregar producto en {rack} - {slot}")

        fila_slot = df[(df['rack'] == rack) & (df['slot'] == slot)]
        if fila_slot.empty:
            fila_data = {
                'rack': rack,
                'slot': slot,
                'producto': '',
                'fecha_vto': '',
                'cantidad': 0,
                'fecha_produccion': '',
                'fecha_acomodado': '',
                'lote': ''
            }
        else:
            fila_data = fila_slot.iloc[0].to_dict()

        with st.form(key="form_editar"):
            producto = st.text_input("Producto", value=fila_data.get('producto', ''))
            fecha_vto = st.date_input("Fecha Vto", value=pd.to_datetime(fila_data.get('fecha_vto')) if fila_data.get('fecha_vto') else None)
            cantidad = st.number_input("Cantidad", min_value=0, value=int(fila_data.get('cantidad', 0)))
            fecha_produccion = st.date_input("Fecha Producción", value=pd.to_datetime(fila_data.get('fecha_produccion')) if fila_data.get('fecha_produccion') else None)
            fecha_acomodado = st.date_input("Fecha Acomodado", value=pd.to_datetime(fila_data.get('fecha_acomodado')) if fila_data.get('fecha_acomodado') else None)
            lote = st.text_input("Lote", value=fila_data.get('lote', ''))

            submitted = st.form_submit_button("Guardar")

        if submitted:
            idx = df[(df['rack'] == rack) & (df['slot'] == slot)].index
            if not idx.empty:
                idx = idx[0]
                df.at[idx, 'producto'] = producto
                df.at[idx, 'fecha_vto'] = fecha_vto.strftime('%Y-%m-%d') if fecha_vto else ''
                df.at[idx, 'cantidad'] = cantidad
                df.at[idx, 'fecha_produccion'] = fecha_produccion.strftime('%Y-%m-%d') if fecha_produccion else ''
                df.at[idx, 'fecha_acomodado'] = fecha_acomodado.strftime('%Y-%m-%d') if fecha_acomodado else ''
                df.at[idx, 'lote'] = lote
            else:
                nuevo = {
                    'rack': rack,
                    'slot': slot,
                    'producto': producto,
                    'fecha_vto': fecha_vto.strftime('%Y-%m-%d') if fecha_vto else '',
                    'cantidad': cantidad,
                    'fecha_produccion': fecha_produccion.strftime('%Y-%m-%d') if fecha_produccion else '',
                    'fecha_acomodado': fecha_acomodado.strftime('%Y-%m-%d') if fecha_acomodado else '',
                    'lote': lote
                }
                df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)

            guardar_datos(df)
            st.success("Datos guardados correctamente.")
            del st.session_state['edit_slot']
            del st.session_state['edit_rack']
            st.info("Por favor, recarga la página para ver los cambios.")

if __name__ == "__main__":
    main()
