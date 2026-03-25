''' App que ofrece informacion estadisticas de los Pokémons y Pemite Realizar y Visualizar Comparaciones entre Pokémons
Ademas de que tienes la posibilidad de realizar carga de nuevos Pokémons y sus caracteristicas, si no los tienes en la DB
Por otro lado, tambien permite modificarlos, eliminarlos, volver a cargarlos, ademas, puedes generar un reporte tipo data
sheet y un reporte de comparaciones entre los Pokémons imprimible paraa coleccionar'''

# app.py

# ---------------------------------- IMPORTACIONES DE LIBRERIAS ----------------------------------------- #
import os
import sys
import time
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------------------------- IMPORTACIONES DE MODULOS ----------------------------------------- #

from database.models import Pokemon
from database.database import SessionLocal
from services.pokemon_service import preload_pokemon_range, get_pokemon_data
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


# ---------------------------------- CONFIGURACIÓN DE PÁGINA ------------------------------- #
st.set_page_config(
    page_title="Pokédex con PokeAPI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------- CSS PERSONALIZADO --------------------------------- #
st.markdown("""
    <style>
    div.stButton > button {
        min-width: 140px;
        font-size: 16px;
        padding: 0.6em 1.2em;
    }
    </style>
""", unsafe_allow_html=True)

TOTAL_POKEMON = 1025
SPRITE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"

# ----------------------------------------- ESTADO INICIAL ----------------------------------------- #
if "loading_pokedex" not in st.session_state:
    st.session_state.loading_pokedex = False
if "preload_index" not in st.session_state:
    st.session_state.preload_index = 1
if "total_time" not in st.session_state:
    st.session_state.total_time = 0
if "pokemon_id" not in st.session_state:
    st.session_state.pokemon_id = 1

# ------------------------------------------ UI PRINCIPAL ----------------------------------------- #
#st.title("Pokédex con PokeAPI")
st.title("📚 Pokedex de Pokémon")

progress_container = st.empty()
modal_container = st.empty()

# -------------------------------------- PRECARGA EN SIDEBAR -------------------------------------- #
with st.sidebar:
     
    # La precarga se hace en el sidebar para que no se bloquee la interfaz
    st.markdown("---", unsafe_allow_html=True)
    st.subheader("⚡Precarga Pokédex")

    # Botón por lotes: Realizar la precarga en lotes de 105 Pokémon a nivel del Backend
    if st.button("Pokédex Por Lotes"):
        st.session_state.loading_pokedex = True
        st.session_state.preload_index = 1
        st.rerun()

    # --- Separador --- #   
    st.markdown("---", unsafe_allow_html=True)

    # La precarga se hace en el sidebar para que no se bloquee la interfaz
    st.subheader("🧰 Pokédex Pull")

    # Botón completa con advertencia: Realizar la precarga completa en lotes de 105 Pokémon y muestra advertencia de que se recomienda usar un equipo con recursos
    if st.button("Pokédex Completa"):
        modal_container.warning(
            "⚠️ Precarga completa/rápida consumirá el doble de recursos. "
            "Tu equipo usará más CPU y memoria durante el proceso. "
            "👉 Recomendado solo en equipos potentes o servidores."
        )
        start_time = time.time()
        preload_pokemon_range(1, TOTAL_POKEMON, max_workers=20)
        elapsed = time.time() - start_time

        # Consultar cuántos Pokémon hay en DB
        db = SessionLocal()
        try:
            saved = db.query(Pokemon).count()
        finally:
            db.close()

        # Barra al 100% para indicar que se cargo todo
        progress_container.progress(1.0, text=f"{saved}/{TOTAL_POKEMON} Pokémon cargados")

        if saved >= TOTAL_POKEMON:
            modal_container.success(f"🎉 Pokédex cargada en {elapsed:.1f}s. ¡Completa!")
        else:
            modal_container.warning(f"⚠️ Precarga incompleta. Pokémon en DB: {saved}")
    st.markdown("---", unsafe_allow_html=True)


# --------------------------------------  PRECARGA AUTOMÁTICA (POR LOTES) -------------------------------------- #

if st.session_state.get("loading_pokedex", False):
    batch_size = 105

    # Spinner activo durante toda la carga para mostrar la carga por lotes
    with st.spinner("⏳ Precargando Pokédex... Esto puede tardar unos minutos"):
        while st.session_state.preload_index <= TOTAL_POKEMON:
            start = st.session_state.preload_index
            end = min(start + batch_size - 1, TOTAL_POKEMON)

            preload_pokemon_range(start, end, max_workers=20)
            st.session_state.preload_index = end + 1

            # Consultar cuántos Pokémon hay en DB
            db = SessionLocal()
            try:
                saved = db.query(Pokemon).count()
            finally:
                db.close()

            # Mostrar avance con números
            st.write(f"✅ Lote {start}-{end} guardado. Pokémon en DB: {saved}")

            # Delay para que se note el avance
            time.sleep(0.5)

    # Al terminar todos los lotes
    st.session_state.loading_pokedex = False
    st.session_state.preload_index = 1

    if saved >= TOTAL_POKEMON:
        st.success("🎉 Pokédex cargada y guardada en MySQL. ¡Completa!")
    else:
        st.warning(f"⚠️ Precarga incompleta. Pokémon en DB: {saved}")


# ----------------------------------------- DATOS DEL POKÉMON -------------------------------------------- #

# Esta seccion carga y muestra el nombre, tipo, altura, peso y evolución del Pokémon seleccionado
if not st.session_state.loading_pokedex:
    pokemon_id = st.session_state.pokemon_id
    db = SessionLocal()
    try:
        pokemon = get_pokemon_data(db, pokemon_id)
    finally:
        db.close()

# Esta seccion se muestran los tabs o secciones de la pagina 
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Pokémon", "📊 Estadísticas", "➕ Agregar Pokémon", "📑 Data Pokémon"])


    # 1 saltos
    #st.markdown("<br>", unsafe_allow_html=True)

    with tab1:
        #st.markdown("<br>", unsafe_allow_html=True)    
        # Layout: sprite grande y tablas más reducidas, igual que en tab4
        col_img, col_stats = st.columns([1, 2])

        with col_img:
            
            # Mostrar imagen y caption desplazados juntos hacia la izquierda usando columnas internas
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---", unsafe_allow_html=True)        
            local_image_path = f"assets/pokemon_images/{pokemon_id}.png"
            img_width = 560
            caption_offset_px = 5   # vertical: positivo sube el caption hacia la imagen
            
            # Proporciones de las columnas internas
            left_ratio = 0.6 
            center_ratio = 1.0 
            right_ratio = 1.4

            inner_left, inner_center, inner_right = st.columns([left_ratio, center_ratio, right_ratio]) 

            with inner_center:
                display_name = pokemon.name[:1].upper() + pokemon.name[1:] if pokemon.name else ""
                local_image_path = f"assets/pokemon_images/{pokemon_id}.png"
                img_src = local_image_path if os.path.exists(local_image_path) else f"{SPRITE_URL}/{pokemon_id}.png"

                # Dos columnas: ID y sprite, igual que tab4
                id_col, img_col = st.columns([0.25, 0.75])
                with id_col:
                    st.markdown(
                        f"""
                        <div style="display:flex;justify-content:flex-end;align-items:center;width:100%;">
                            <span style="font-size:clamp(0.8em, 1vw, 1.2em);font-weight:bold;white-space:nowrap;">
                                #{pokemon_id}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with img_col:
                    st.image(img_src, use_container_width=True)

        # -------------------------------------- Texto Dinamico del Sprite Pokedex --------------------------------- #

            st.markdown(
                f"""
                <div style="width:100%;margin:0 auto;text-align:center;margin-top:-{caption_offset_px}px;">
                  <h3 style="margin:0;font-weight:600;font-size:clamp(1em, 2vw, 1.5em);">
                    {pokemon.name.capitalize()}
                  </h3>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ---------------------------------------------- Barra de Navegación ------------------------------------------ #

            # 1 saltos
            #st.markdown("<br>", unsafe_allow_html=True)
            pokemon_selector = st.slider(
                "",
                min_value=1,
                max_value=TOTAL_POKEMON,
                value=st.session_state.pokemon_id,
                step=1
            )

            st.markdown(
                        """
                        <div style='text-align: center; margin-top: 20px;'>
                            <p style='font-size:18px; font-weight:bold;'>Desliza para seleccionar un Pokémon</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            if pokemon_selector != st.session_state.pokemon_id:
                st.session_state.pokemon_id = pokemon_selector
                st.rerun()
            #st.markdown("<br><br>", unsafe_allow_html=True)  
            #st.markdown("---", unsafe_allow_html=True)

        # ----------------------------------Botones Adelante y Atras para Navegación --------------------------------- #
            
            # 2 saltos
            st.markdown("<br><br>", unsafe_allow_html=True)

            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
            with col_btn1:
                if st.button("⬅ Anterior"):
                    if st.session_state.pokemon_id > 1:
                        st.session_state.pokemon_id -= 1
                        st.rerun()
            with col_btn2:
                if st.button("Adelante ➡"):
                    if st.session_state.pokemon_id < TOTAL_POKEMON:
                        st.session_state.pokemon_id += 1
                        st.rerun()
            #st.markdown("---")

# -------------------------------------------------- Col STATS (solo el título "Características") ---------------------------------------------- #

# Mostrar las características en forma de data grid (tabla) alineada en 2 columnas
with col_stats:
    st.markdown("<br>", unsafe_allow_html=True)
    # Helper para formatear valores (listas -> coma separada)
    def _fmt(val):
        return ", ".join(map(str, val)) if isinstance(val, (list, tuple)) else str(val)

    # Preparar valores dinámicos
    hp = _fmt(pokemon.hp)
    attack = _fmt(pokemon.attack)
    defense = _fmt(pokemon.defense)
    sp_atk = _fmt(pokemon.special_attack)
    sp_def = _fmt(pokemon.special_defense)
    speed = _fmt(pokemon.speed)
    tipos = _fmt(pokemon.types)
    habilidades = _fmt(pokemon.abilities)

    # Filas para cada columna (ordenadas para que Defense quede bajo Sp. Attack y Speed bajo Sp. Defense)
    left_rows = [("HP", hp), ("Sp. Attack", sp_atk), ("Defense", defense)]
    right_rows = [("Attack", attack), ("Sp. Defense", sp_def), ("Speed", speed)]

    # Construir DataFrame con 4 columnas: Etiqueta A, Valor A, Etiqueta B, Valor B
    rows = []
    max_len = max(len(left_rows), len(right_rows))
    for i in range(max_len):
        la, va = left_rows[i] if i < len(left_rows) else ("", "")
        lb, vb = right_rows[i] if i < len(right_rows) else ("", "")
        rows.append({"Etiqueta A": la, "Valor A": va, "Etiqueta B": lb, "Valor B": vb})

    df = pd.DataFrame(rows)

    st.markdown("---", unsafe_allow_html=True)  
    # Mostrar la tabla (data grid)
    st.title("Poderes del Pokémon")
    st.dataframe(df, use_container_width=True)
    st.markdown("---", unsafe_allow_html=True)

# -------- Mostrar Tipos y Habilidades debajo como una pequeña tabla para mantener consistencia visual --------- #

    #st.markdown("-------", unsafe_allow_html=True) # Separador
    st.title("Características Especiales del Pokémon")
    meta_df = pd.DataFrame({
        "Propiedad": ["Tipos", "Habilidades"],
        "Valor": [tipos, habilidades]
    
    })
    st.table(meta_df)
    #st.markdown("---", unsafe_allow_html=True)

# ---------------------------------------------------- SECCIÓN PAGINA 2 ----------------------------------------- #



# -------------------------------------------------- SECCION ESTADISTICAS --------------------------------------- #
with tab2:
    
    # 1 saltos
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📊 Comparativa de Pokémon")

    # Sliders alineados al ancho de las tablas (centro 90%)
    col_sl_a, col_sl_b = st.columns(2)

    with col_sl_a:
        slider_cols_a = st.columns([0.05, 0.90, 0.05])
        with slider_cols_a[1]:
            low_id = st.slider("Pokémon 1", 1, TOTAL_POKEMON, 1, key="slider_low")

    with col_sl_b:
        slider_cols_b = st.columns([0.05, 0.90, 0.05])
        with slider_cols_b[1]:
            high_id = st.slider("Pokémon 2", 1, TOTAL_POKEMON, TOTAL_POKEMON, key="slider_high")

    # Obtener datos de ambos Pokémon (una vez, después de los sliders)
    db = SessionLocal()
    try:
        pokemon_low = get_pokemon_data(db, low_id)
        pokemon_high = get_pokemon_data(db, high_id)
    finally:
        db.close()

    # Preparar stats para gráficos
    labels = ["HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]
    vals_low = [pokemon_low.hp, pokemon_low.attack, pokemon_low.defense,
                pokemon_low.special_attack, pokemon_low.special_defense, pokemon_low.speed]
    vals_high = [pokemon_high.hp, pokemon_high.attack, pokemon_high.defense,
                 pokemon_high.special_attack, pokemon_high.special_defense, pokemon_high.speed]

    max_val = max(max(vals_low), max(vals_high), 1)
    y_max = int(np.ceil(max_val / 10.0) * 10)

    def _plot_lines(ax, x_labels, main_vals, other_vals, main_label, other_label, color_main="#e63946"):
        x = np.arange(len(x_labels))
        ax.plot(x, other_vals, label=other_label, color="#999999", linewidth=1.5, linestyle="--", marker="o", alpha=0.6)
        ax.plot(x, main_vals, label=main_label, color=color_main, linewidth=3, marker="o", alpha=0.95)
        ax.fill_between(x, other_vals, alpha=0.05, color="#999999")
        ax.fill_between(x, main_vals, alpha=0.12, color=color_main)
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, rotation=25, ha="right")
        ax.set_ylim(0, y_max)
        ax.grid(axis="y", linestyle=":", alpha=0.6)
        ax.legend(fontsize=8, loc="upper right")


# ----------------------------------------------------- Bloques visuales (Col A y Col B)  ------------------------------------------ #
    
    colA, colB = st.columns(2)

    # ----- Col A (contenido alineado a la izquierda)  ----- #
    with colA:
        inner_left = st.columns([0.85, 0.15])  # contenido en inner_left[0] => más a la izquierda
        with inner_left[0]:
            content = st.columns([0.54, 0.46])
            with content[0]:
                st.image(f"{SPRITE_URL}/{low_id}.png", width=300)
            with content[1]:
                fig, ax = plt.subplots(figsize=(4.0, 3.2))
                _plot_lines(ax, labels, vals_low, vals_high, pokemon_low.name, pokemon_high.name, color_main="#1f77b4")
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            # Tabla A: usar la misma proporción central que el slider
            table_cols = st.columns([0.05, 0.90, 0.05])
            
            # Tabla A (reemplaza el st.dataframe de la Tabla A)
            with table_cols[1]:
                st.markdown(
                    f'<h3 style="margin:4px 0 6px 0; font-size:18px; font-weight:600;">Estadísticas de {pokemon_low.name}</h3>',
                    unsafe_allow_html=True
                )
                df_low = pd.DataFrame({"Stat": labels, "Value": vals_low})

                # Cálculo de altura exacta según filas (ajusta row_height si tus filas son más altas)
                rows = len(df_low)
                row_height = 28            # px por fila (ajusta si necesitas)
                header_px = 36             # espacio para el encabezado del dataframe
                padding_px = 8             # pequeño margen extra
                height_px = rows * row_height + header_px + padding_px

                st.dataframe(df_low.style.set_properties(subset=["Value"], **{"text-align":"center"}), use_container_width=True, height=height_px)


    # ----- Col B (contenido alineado a la derecha) ----- #
    with colB:
        inner_right = st.columns([0.15, 0.85])  # contenido en inner_right[1] => más a la derecha
        with inner_right[1]:
            content_r = st.columns([0.54, 0.46])
            with content_r[0]:
                st.image(f"{SPRITE_URL}/{high_id}.png", width=300)
            with content_r[1]:
                fig2, ax2 = plt.subplots(figsize=(4.0, 3.2))
                _plot_lines(ax2, labels, vals_high, vals_low, pokemon_high.name, pokemon_low.name, color_main="#e63946")
                fig2.tight_layout()
                st.pyplot(fig2, use_container_width=True)
                plt.close(fig2)

            # Tabla B: usar la misma proporción central que el slider
            table_cols_r = st.columns([0.05, 0.90, 0.05])
            
            # Tabla B (reemplaza el bloque actual)
            with table_cols_r[1]:
                st.markdown(
                    f'<h3 style="margin:4px 0 6px 0; font-size:18px; font-weight:600;">Estadísticas de {pokemon_high.name}</h3>',
                    unsafe_allow_html=True
                )
                df_high = pd.DataFrame({"Stat": labels, "Value": vals_high})

                rows = len(df_high)
                row_height = 28
                header_px = 36
                padding_px = 8
                height_px = rows * row_height + header_px + padding_px

                st.dataframe(df_high.style.set_properties(subset=["Value"], **{"text-align":"center"}), use_container_width=True, height=height_px)

# --------------------------------------------------------- TABLA DE POKÉMON 3 ------------------------------------------------------ #
with tab3:
    st.markdown("<h2 style='text-align:center;'>➕ Gestión de Pokémon</h2>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    # ------------------------- Fila superior: Agregar + Data Grid ------------------------- #
    col_add, col_grid = st.columns([1, 1])
    with col_add:
        st.subheader("Agregar un nuevo Pokémon a la Pokédex")

        form_col1, form_col2 = st.columns(2)
        with form_col1:
            new_id = st.number_input("ID del Pokémon", min_value=TOTAL_POKEMON+1, step=1)
            new_name = st.text_input("Nombre")
            new_hp = st.number_input("HP", min_value=1)
            new_attack = st.number_input("Attack", min_value=1)
            new_defense = st.number_input("Defense", min_value=1)
            new_height = st.number_input("Altura", min_value=1)
            new_weight = st.number_input("Peso", min_value=1)
        with form_col2:
            new_special_attack = st.number_input("Sp. Attack", min_value=1)
            new_special_defense = st.number_input("Sp. Defense", min_value=1)
            new_speed = st.number_input("Velocidad", min_value=1)
            new_generation = st.text_input("Generación")
            new_region = st.text_input("Región")
            new_types = st.text_input("Tipos (separados por coma)")
            new_abilities = st.text_input("Habilidades (separadas por coma)")

        uploaded_file = st.file_uploader("Selecciona imagen del Pokémon (.jpg o .png)", type=["jpg", "png"])

        if st.button("Guardar Pokémon"):
            # 👇 Validaciones
            if not new_name.strip():
                st.error("⚠ Debes ingresar un nombre para el Pokémon")
            elif not new_types.strip():
                st.error("⚠ Debes ingresar al menos un tipo")
            elif not new_abilities.strip():
                st.error("⚠ Debes ingresar al menos una habilidad")
            elif any(stat < 1 for stat in [new_hp, new_attack, new_defense, new_special_attack, new_special_defense, new_speed]):
                st.error("⚠ Todas las estadísticas deben ser mayores a 0")
            else:
                db = SessionLocal()
                try:
                    # Verificar si ya existe un Pokémon con ese ID
                    existing = db.query(Pokemon).filter(Pokemon.id == new_id).first()
                    if existing:
                        st.error(f"⚠ Ya existe un Pokémon con ID {new_id}. Usa otro ID o edítalo en 'Modificar Pokémon'.")
                    else:
                        pokemon = Pokemon(
                            id=new_id,
                            name=new_name,
                            height=new_height,
                            weight=new_weight,
                            hp=new_hp,
                            attack=new_attack,
                            defense=new_defense,
                            special_attack=new_special_attack,
                            special_defense=new_special_defense,
                            speed=new_speed,
                            types=new_types,
                            abilities=new_abilities,
                            generation=new_generation,
                            region=new_region,
                        )
                        db.add(pokemon)
                        db.commit()

                        # Guardar imagen si se subió
                        os.makedirs("assets/pokemon_images", exist_ok=True)

                        if uploaded_file is not None:
                            try:
                                from PIL import Image
                                save_path = os.path.join("assets/pokemon_images", f"{new_id}.png")

                                image = Image.open(uploaded_file)
                                image = image.resize((300, 300))
                                image.save(save_path)

                                # Actualizar ruta en la BD
                                pokemon.image_path = save_path
                                db.commit()

                                st.success(f"✅ Pokémon {new_name} agregado con imagen en {save_path}")
                            except Exception as img_err:
                                # Si falla el guardado de la imagen, informar pero mantener el registro en BD
                                st.warning(f"⚠ Pokémon guardado pero ocurrió un error al procesar la imagen: {img_err}")
                                st.success(f"✅ Pokémon {new_name} agregado sin imagen (registro guardado).")
                        else:
                            st.success("✅ Pokémon guardado sin imagen")
                except Exception as e:
                    db.rollback()
                    st.error(f"❌ Error al guardar el Pokémon: {e}")
                finally:
                    db.close()
        st.markdown("---", unsafe_allow_html=True)

# --------------------------------------------------------- TABLA DE POKÉMON REGISTRADOS TAB-3 ------------------------------------------------------ #
    with col_grid:
        st.subheader("📋 Pokémon registrados")
        st.markdown("---", unsafe_allow_html=True)
        db = SessionLocal()
        try:
            pokemons = db.query(Pokemon).all()
            if pokemons:
                df = pd.DataFrame([{
                    "ID": p.id,
                    "Nombre": p.name,
                    "HP": p.hp,
                    "Attack": p.attack,
                    "Defense": p.defense,
                    "Speed": p.speed,
                    "Región": p.region
                } for p in pokemons])
                # 👉 Ajustamos la altura del grid
                st.dataframe(df, use_container_width=True, height=682)
            else:
                st.info("No hay Pokémon registrados aún.")
        finally:
            db.close()
        st.markdown("---", unsafe_allow_html=True)

# --------------------------------- Modificar Pokémon existente (bloque con validaciones completas) ----------------------------------------- #
    
    col_edit, col_delete = st.columns([1, 1])

    with col_edit:
        st.markdown("---", unsafe_allow_html=True)
        st.subheader("✏️ Modificar Pokémon existente")
        edit_id = st.number_input("ID del Pokémon a modificar", min_value=1, step=1)

        # Botón para cargar: al pulsarlo buscamos en la DB y guardamos en session_state si existe
        if st.button("Cargar Pokémon"):
            db = SessionLocal()
            try:
                pokemon = db.query(Pokemon).filter(Pokemon.id == edit_id).first()
                if pokemon:
                    st.session_state.loaded_edit_id = edit_id
                    st.session_state.loaded_edit_name = pokemon.name or ""
                    st.session_state.loaded_edit_hp = pokemon.hp or 0
                    st.session_state.loaded_edit_attack = pokemon.attack or 0
                    st.session_state.loaded_edit_defense = pokemon.defense or 0
                    st.session_state.loaded_edit_height = pokemon.height or 0
                    st.session_state.loaded_edit_weight = pokemon.weight or 0
                    st.session_state.loaded_edit_spatk = pokemon.special_attack or 0
                    st.session_state.loaded_edit_spdef = pokemon.special_defense or 0
                    st.session_state.loaded_edit_speed = pokemon.speed or 0
                    st.session_state.loaded_edit_generation = pokemon.generation or ""
                    st.session_state.loaded_edit_region = pokemon.region or ""
                    st.session_state.loaded_edit_types = pokemon.types or ""
                    st.session_state.loaded_edit_abilities = pokemon.abilities or ""
                    st.success(f"✅ Pokémon con ID {edit_id} cargado. Edita los campos y guarda los cambios.")
                else:
                    for k in list(st.session_state.keys()):
                        if k.startswith("loaded_edit_"):
                            del st.session_state[k]
                    st.warning(f"⚠ No se encontró Pokémon con ID {edit_id}.")
            finally:
                db.close()

        # Si hay un Pokémon cargado en session_state y coincide con edit_id, mostramos el formulario de edición
        if st.session_state.get("loaded_edit_id", None) == edit_id:
            key_prefix = f"edit_{edit_id}_"

            new_name = st.text_input("Nombre", value=st.session_state.get("loaded_edit_name", ""), key=key_prefix + "name")
            new_hp = st.number_input("HP", min_value=0, value=st.session_state.get("loaded_edit_hp", 0), key=key_prefix + "hp")
            new_attack = st.number_input("Attack", min_value=0, value=st.session_state.get("loaded_edit_attack", 0), key=key_prefix + "attack")
            new_defense = st.number_input("Defense", min_value=0, value=st.session_state.get("loaded_edit_defense", 0), key=key_prefix + "defense")
            new_height = st.number_input("Altura", min_value=0, value=st.session_state.get("loaded_edit_height", 0), key=key_prefix + "height")
            new_weight = st.number_input("Peso", min_value=0, value=st.session_state.get("loaded_edit_weight", 0), key=key_prefix + "weight")
            new_special_attack = st.number_input("Sp. Attack", min_value=0, value=st.session_state.get("loaded_edit_spatk", 0), key=key_prefix + "spatk")
            new_special_defense = st.number_input("Sp. Defense", min_value=0, value=st.session_state.get("loaded_edit_spdef", 0), key=key_prefix + "spdef")
            new_speed = st.number_input("Velocidad", min_value=0, value=st.session_state.get("loaded_edit_speed", 0), key=key_prefix + "speed")
            new_generation = st.text_input("Generación", value=st.session_state.get("loaded_edit_generation", ""), key=key_prefix + "generation")
            new_region = st.text_input("Región", value=st.session_state.get("loaded_edit_region", ""), key=key_prefix + "region")
            new_types = st.text_input("Tipos (separados por coma)", value=st.session_state.get("loaded_edit_types", ""), key=key_prefix + "types")
            new_abilities = st.text_input("Habilidades (separadas por coma)", value=st.session_state.get("loaded_edit_abilities", ""), key=key_prefix + "abilities")

            uploaded_file = st.file_uploader("Actualizar imagen del Pokémon (.jpg o .png)", type=["jpg", "png"], key=key_prefix + "upload")

            # ✅ Confirmación explícita (igual que en eliminar)
            confirm_mod = st.checkbox("✅ Confirmo que deseo modificar este Pokémon", key=key_prefix + "confirm_mod")

            if st.button("Guardar cambios", key=key_prefix + "save"):
                if not confirm_mod:
                    st.error("⚠ Debes confirmar la modificación antes de continuar")
                else:
                    # 👇 Aquí van las validaciones y la lógica de actualización
                    db = SessionLocal()
                    try:
                        pokemon = db.query(Pokemon).filter(Pokemon.id == edit_id).first()
                        if not pokemon:
                            st.error("⚠ El Pokémon ya no existe en la base de datos.")
                        else:
                            # Actualizar campos
                            pokemon.name = new_name.strip()
                            pokemon.hp = int(new_hp)
                            pokemon.attack = int(new_attack)
                            pokemon.defense = int(new_defense)
                            pokemon.height = int(new_height)
                            pokemon.weight = int(new_weight)
                            pokemon.special_attack = int(new_special_attack)
                            pokemon.special_defense = int(new_special_defense)
                            pokemon.speed = int(new_speed)
                            pokemon.types = new_types.strip()
                            pokemon.abilities = new_abilities.strip()
                            pokemon.generation = new_generation.strip()
                            pokemon.region = new_region.strip()
                            db.commit()

                            # Actualizar imagen si se sube una nueva
                            if uploaded_file is not None:
                                try:
                                    from PIL import Image
                                    os.makedirs("assets/pokemon_images", exist_ok=True)
                                    save_path = os.path.join("assets/pokemon_images", f"{edit_id}.png")

                                    image = Image.open(uploaded_file).convert("RGBA")
                                    image = image.resize((300, 300))
                                    image.save(save_path)

                                    try:
                                        pokemon.image_path = save_path
                                        db.commit()
                                    except Exception:
                                        pass
                                except Exception as img_err:
                                    st.warning(f"⚠ Pokémon actualizado pero ocurrió un error al procesar la imagen: {img_err}")

                            st.success(f"✅ Pokémon con ID {edit_id} actualizado correctamente")

                            # Limpiar session_state
                            for k in list(st.session_state.keys()):
                                if k.startswith("loaded_edit_"):
                                    del st.session_state[k]
                    except Exception as e:
                        db.rollback()
                        st.error(f"❌ Error al actualizar el Pokémon: {e}")
                    finally:
                        db.close()
            st.markdown("---")
            #st.subheader("🗑 Eliminar Pokémon existente")

    # ------------------------------------------------------- Eliminar Pokemon --------------------------------------------------------- #
    
    with col_delete:
        st.markdown("---", unsafe_allow_html=True)
        st.subheader("🗑 Eliminar Pokémon de la Pokédex")
        delete_id = st.number_input("ID del Pokémon a eliminar", min_value=1, step=1)
        # 👇 Confirmación explícita
        confirm_delete = st.checkbox("✅ Confirmo que deseo eliminar este Pokémon")

        if st.button("Eliminar Pokémon"):
            if not confirm_delete:
                st.error("⚠ Debes confirmar la eliminación antes de continuar")
            else:
                db = SessionLocal()
                try:
                    pokemon = db.query(Pokemon).filter(Pokemon.id == delete_id).first()
                    if pokemon:
                        db.delete(pokemon)
                        db.commit()

                        # 👇 Eliminar imagen asociada si existe
                        import os
                        image_path = os.path.join("assets/pokemon_images", f"{delete_id}.png")
                        if os.path.exists(image_path):
                            os.remove(image_path)

                        st.success(f"✅ Pokémon con ID {delete_id} eliminado de la Pokédex")
                    else:
                        st.warning(f"⚠ No se encontró Pokémon con ID {delete_id}")
                finally:
                    db.close()

# --------------------------------------------------------- Tabla de Pokémon 4  ------------------------------------------------------ #
        from fpdf import FPDF
        import os

        def generar_pdf(pokemon, img_src):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Título
            pdf.cell(200, 10, txt=f"Data Sheet - {pokemon.name}", ln=True, align="C")

            # Datos
            datos = [
                ("ID", pokemon.id),
                ("Nombre", pokemon.name),
                ("HP", pokemon.hp),
                ("Attack", pokemon.attack),
                ("Defense", pokemon.defense),
                ("Sp. Attack", pokemon.special_attack),
                ("Sp. Defense", pokemon.special_defense),
                ("Speed", pokemon.speed),
                ("Altura", pokemon.height),
                ("Peso", pokemon.weight),
                ("Tipos", pokemon.types),
                ("Habilidades", pokemon.abilities),
                ("Generación", pokemon.generation),
                ("Región", pokemon.region),
            ]

            for campo, valor in datos:
                pdf.cell(0, 10, txt=f"{campo}: {valor}", ln=True)

            # Sprite
            if os.path.exists(img_src):
                pdf.image(img_src, x=60, y=pdf.get_y()+10, w=80)

            # ✅ Devuelve bytes en lugar de intentar encode
            return bytes(pdf.output(dest="S"))

        with tab4:
            # Título centrado
            st.markdown("<h2 style='text-align: center;'>📑 Data Pokémon</h2>", unsafe_allow_html=True)

            # Inputs para cargar Pokémon por ID o Nombre
            st.markdown("### 🔎 Buscar Pokémon")
            col_id, col_name = st.columns([1, 2])
            with col_id:
                input_id = st.number_input("ID del Pokémon", min_value=1, step=1, value=st.session_state.pokemon_id)
            with col_name:
                input_name = st.text_input("Nombre del Pokémon").strip()

            # Obtener datos según búsqueda
            db = SessionLocal()
            try:
                if input_name:
                    pokemon = db.query(Pokemon).filter(Pokemon.name.ilike(f"%{input_name}%")).first()
                else:
                    pokemon = get_pokemon_data(db, input_id)
            finally:
                db.close()

            if pokemon:
                # Dividir en dos columnas: tabla más amplia y sprite más reducido
                col_data, col_sprite = st.columns([2, 1])  # tabla ocupa 2/3, sprite 1/3

                with col_data:
                    st.markdown("### 📋 Hoja de Datos Principal")
                    data = {
                        "ID": pokemon.id,
                        "Nombre": pokemon.name,
                        "HP": pokemon.hp,
                        "Attack": pokemon.attack,
                        "Defense": pokemon.defense,
                        "Sp. Attack": pokemon.special_attack,
                        "Sp. Defense": pokemon.special_defense,
                        "Speed": pokemon.speed,
                        "Altura": pokemon.height,
                        "Peso": pokemon.weight,
                        "Tipos": pokemon.types,
                        "Habilidades": pokemon.abilities,
                        "Generación": pokemon.generation,
                        "Región": pokemon.region,
                    }
                    st.table(pd.DataFrame(data.items(), columns=["Campo", "Valor"]))

                with col_sprite:
                    st.markdown("<h2 style='text-align: center;'> 🎨 Sprite del Pokémon </h2>", unsafe_allow_html=True)
                    local_image_path = f"assets/pokemon_images/{pokemon.id}.png"
                    img_src = local_image_path if os.path.exists(local_image_path) else f"{SPRITE_URL}/{pokemon.id}.png"
                    st.image(img_src, use_container_width=True, caption=pokemon.name.capitalize())

                    
                    # Botón de descarga PDF para el grid principal
                    pdf_bytes = generar_pdf(pokemon, img_src)

                    # Crear tres columnas iguales y poner el botón en la del medio
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            label="📄 Data Sheet en PDF",
                            data=pdf_bytes,
                            file_name=f"{pokemon.name}_datasheet.pdf",
                            mime="application/pdf"
                        )

            else:
                st.warning("⚠ No se encontró ningún Pokémon con ese ID o Nombre.")

            # Bloque de filtros al pie
            st.markdown("---")
            st.markdown("<h2 style='text-align: center;'>📑Filtrado de Pokémons </h2>", unsafe_allow_html=True)
            st.info("👉 Usa este grid para filtrar datos del Pokémon por ID o Nombre, o seleccionar campos específicos.")

            # Inputs de filtro por ID y Nombre
            col_id_f, col_name_f = st.columns([1, 2])
            with col_id_f:
                filtro_id = st.number_input("Filtrar por ID", min_value=1, step=1)
            with col_name_f:
                filtro_name = st.text_input("Filtrar por Nombre").strip()

            # Obtener datos según filtro
            db = SessionLocal()
            try:
                if filtro_name:
                    pokemon_filtrado = db.query(Pokemon).filter(Pokemon.name.ilike(f"%{filtro_name}%")).first()
                elif filtro_id > 0:
                    pokemon_filtrado = get_pokemon_data(db, filtro_id)
                else:
                    pokemon_filtrado = None
            finally:
                db.close()

            if pokemon_filtrado:
                # Misma proporción de columnas que el grid principal
                col_data_f, col_sprite_f = st.columns([2, 1])

                with col_data_f:
                    st.markdown("### 📋 Datos Filtrados")
                    data_f = {
                        "ID": pokemon_filtrado.id,
                        "Nombre": pokemon_filtrado.name,
                        "HP": pokemon_filtrado.hp,
                        "Attack": pokemon_filtrado.attack,
                        "Defense": pokemon_filtrado.defense,
                        "Sp. Attack": pokemon_filtrado.special_attack,
                        "Sp. Defense": pokemon_filtrado.special_defense,
                        "Speed": pokemon_filtrado.speed,
                        "Altura": pokemon_filtrado.height,
                        "Peso": pokemon_filtrado.weight,
                        "Tipos": pokemon_filtrado.types,
                        "Habilidades": pokemon_filtrado.abilities,
                        "Generación": pokemon_filtrado.generation,
                        "Región": pokemon_filtrado.region,
                    }

                    # Multiselect para campos opcionales
                    campos = list(data_f.keys())
                    seleccion = st.multiselect("Selecciona los campos que deseas mostrar", campos)
                    if seleccion:
                        filtrado = {k: data_f[k] for k in seleccion}
                        st.table(pd.DataFrame(filtrado.items(), columns=["Campo", "Valor"]))
                    else:
                        st.table(pd.DataFrame(data_f.items(), columns=["Campo", "Valor"]))

                with col_sprite_f:
                    st.markdown("<h3>", unsafe_allow_html=True)
                    st.markdown("<h2 style='text-align: center;'>🎨 Sprite Filtrado</h2>", unsafe_allow_html=True)
                    local_image_path = f"assets/pokemon_images/{pokemon_filtrado.id}.png"
                    img_src = local_image_path if os.path.exists(local_image_path) else f"{SPRITE_URL}/{pokemon_filtrado.id}.png"
                    st.image(img_src, use_container_width=True, caption=pokemon_filtrado.name.capitalize())

                    # Botón de descarga PDF para el grid filtrado
                    pdf_bytes = generar_pdf(pokemon_filtrado, img_src)

                    col1, col2, col3 = st.columns([1, 1, 1])  # tres columnas iguales
                    with col2:
                        st.download_button(
                            label="📄 Data Sheet Filtrado en PDF",
                            data=pdf_bytes,
                            file_name=f"{pokemon_filtrado.name}_datasheet.pdf",
                            mime="application/pdf"
                        )

# ------------------------------------ Utilidades y Herramientas en La Web --------------------------------------------------------- #
            st.markdown("""
                <style>
                @media print {
                    body { background: white; }
                    img { max-width: 300px; }
                    table { font-size: 12pt; }
                }
                </style>
                
            """, unsafe_allow_html=True)

# ----------------------------------------------------------- La Web --------------------------------------------------------------- #
       
st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; font-size: 13px; color: gray;'>
        © 2026 Todos los derechos reservados.<br>
        Proyecto de Ingeniería de Software - Licencia Limitada.<br>
        Desarrollado por: <b>Victor Miletic</b><br>
        Repositorio: <a href='https://github.com/Viktorostermann/Python' target='_blank'>GitHub</a><br>
        Contacto: <a href='mailto:'>viktoremiletic@gmail.com</a>
    </div>
    
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <!-- Bloque de iconos alineados a la izquierda -->
        <div style='text-align: right;'>
            <a href="https://www.linkedin.com/in/tuusuario" target="_blank" style="margin-right:15px;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30">
            </a>
            <a href="https://wa.me/51999999999" target="_blank" style="margin-right:15px;">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="30">
            </a>
            <a href="https://www.youtube.com/@tuusuario" target="_blank" style="margin-right:15px;">
                <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="30">
            </a>
            <a href="https://www.facebook.com/tuusuario" target="_blank" style="margin-right:15px;">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="30">
            </a>
            <a href="https://x.com/tuusuario" target="_blank" style="margin-right:15px;">
                <img src="https://cdn-icons-png.flaticon.com/512/5968/5968833.png" width="30">


</a>

    """,
    unsafe_allow_html=True
)
st.markdown("---")