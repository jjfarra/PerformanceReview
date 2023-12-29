import streamlit as st
import pandas as pd
import plotly.graph_objects as go
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .ea3mdgi4 {
            padding-top: 30px;
            padding-right: 30px;
            padding-bottom: 50px;
            padding-left: 50px;
        }
    </style>
""", unsafe_allow_html=True)


def generate_gauge_chart(data, column_name, title, width, height):
    value = data[column_name].values[0]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={"x": [0, 1], "y": [0, 1]},
        title={'text': title},
        gauge={
            "axis": {"range": [0, 100]},
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": value
            }
        }
    ))
    fig.update_layout(width=width, height=height)
    with st.container():
        st.plotly_chart(fig)


def create_info_container(data, columns):
    with st.container():
        cols = st.columns(len(columns))
        for idx in range(0, len(columns)):
            title = "AÑO" if columns[idx] == "anio" else columns[idx].replace("_", " ").upper()
            with cols[idx]:
                st.subheader(f"**{title}** ", anchor=False)
                st.write(f"{data[columns[idx]].values[0]}")


def create_graph_per_activity(data, title, columns):

    with st.container():
        st.header(title.capitalize(), anchor=False)
        cols = st.columns(len(columns))
        for idx in range(0, len(columns)):
            with cols[idx]:
                generate_gauge_chart(data, columns[idx], f"# {idx+1}", 200, 350)

    st.write("---")


def create_tabs(data, page, info, columns):

    with page:
        year, period = info.split("-")
        selected_student_data = data[data.anio == int(year)][data.periodo == period]
        st.markdown("""
            <style>
                div[data-testid="column"] h3 {
                        text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)
        first_block = ["matricula", "estudiante", "carrera", "paralelo", "vez_tomada"]
        create_info_container(selected_student_data, first_block)

        st.markdown("""
                       <style>
                           .e1nzilvr5 p{
                                   text-align: center;
    
                       }
                   </style>
                   """, unsafe_allow_html=True)
        second_block = ["anio", "periodo", "profesor", "estado"]
        create_info_container(selected_student_data, second_block)
        st.write("---")

        with st.container():
            st.subheader("Notas Obtenidas", anchor=False)
            theoretical, practice = st.columns(2)
            with theoretical:
                generate_gauge_chart(selected_student_data, "nota_teorico", "Nota Teórica", 450, 350)
            with practice:
                generate_gauge_chart(selected_student_data, "nota_practico", "Nota Practico", 450, 350)
        st.write("---")

        create_graph_per_activity(selected_student_data, "Lecciones", columns["lesson_columns"])
        create_graph_per_activity(selected_student_data, "Talleres", columns["workshop_columns"])
        create_graph_per_activity(selected_student_data, "Examenes", columns["exam_columns"])

        st.markdown("""
           <style>
               .e1nzilvr1 {
                       text-align: center;
           }
           .e1vs0wn30{
                align-items: center;
           }
            </style>
       """, unsafe_allow_html=True)


def selfcomparative_graphs(columns, data, title):
    with st.container():
        st.markdown(f"""
                    <div font-size: 50px;>
                    <span>{title.upper()}</span>
                    </div>
                    """, unsafe_allow_html=True)
        fig = go.Figure()
        grouped = data.groupby("year_period")

        for year, group in grouped:
            fig.add_trace(
                go.Scatter(
                    x=columns,
                    y=group[columns].mean(),
                    name=str(year),
                    mode="lines+markers"
                )
            )
        name_columns = []
        for col in columns:
            name_columns.append(col.replace("_", " ").upper())

        fig.update_layout(
            title=f"Puntajes por {title.capitalize()} en Diferentes Periodos",
            xaxis_title=title.upper(),
            yaxis_title="Puntaje Promedio",
            xaxis=dict(tickvals=[0, 1, 2, 3], ticktext=name_columns),
            legend=dict(title="Año"),
        )

        st.plotly_chart(fig)


def comparative_graphs(columns, data, title):
    print("Hola")

dashboard = st.empty()
dashboard.title("Performance Review Programming Fundamentals", anchor=False)
dashboard.write("Upload Actual Performance CSV",)
actual_file = dashboard.file_uploader("actual_performance", ["csv"],
                                      accept_multiple_files=False, key="actual_performance", label_visibility="hidden")
comparative_categories = ["Consigo mismo","Veces Tomada", "Paralelo", "Carrera", "Tipo", "Novatos", "Todos"]
if actual_file is not None:
    dashboard.empty()
    dataframe = pd.read_csv(actual_file, sep=";")
    st.title("Programming Fundamentals Review".upper(), anchor=False)

    if "selected_comparative" not in st.session_state:
        st.session_state.selected_comparative = comparative_categories[0]

    def on_select_student_change():
        st.session_state.selected_comparative = comparative_categories[0]

    with st.sidebar.container():
        selected_student = st.selectbox("Elija un estudiante:", dataframe["estudiante"].unique(),on_change=on_select_student_change)
        selected_comparative = st.selectbox("Elija una comparativa", comparative_categories,key="selected_comparative")

        st.markdown("""
            <style>
                .eczjsme4 {  
                    padding-top: 10px;
                    padding-right: 10px;
                    padding-bottom: 30px;
                    padding-left: 10px;
                }
            </style>
        """, unsafe_allow_html=True)
    student_data = dataframe[dataframe.estudiante == selected_student].fillna(0)
    student_data["estado"] = student_data.apply(
        lambda x: "AP" if((x.nota_teorico*0.7)+(x.nota_practico*0.3)) > 60 else "RP", axis=1)
    student_data = student_data.sort_values(by="anio", ascending=False).reset_index(drop=True)
    activities = {"lesson_columns": ["leccion_1", "leccion_2", "leccion_3", "leccion_4"],
                  "exam_columns": ["examen_parcial", "examen_final", "examen_mejoramiento"],
                  "workshop_columns": ["taller_1", "taller_2", "taller_3", "taller_4"]
                  }
    st.markdown("""
        <div font-size: 200px;>
            <span>STUDENT INFORMATION</span>
        </div>
    """, unsafe_allow_html=True)
    years_period = [f"{str(row.anio)}-{row.periodo}" for idx, row in student_data.iterrows()]
    student_data["year_period"] = years_period
    years_period.append(f"COMPARATIVA {selected_comparative.upper()}")
    tabs = st.tabs(years_period)
    
    for tab in tabs[:-1]:
        with tab:
            create_tabs(student_data, tab, years_period[tabs.index(tab)], activities)

    with tabs[-1]:
        selfcomparative_graphs(activities["lesson_columns"], student_data, "Lecciones")
        selfcomparative_graphs(activities["workshop_columns"], student_data, "Talleres")
        selfcomparative_graphs(activities["exam_columns"], student_data, "Exámenes")
