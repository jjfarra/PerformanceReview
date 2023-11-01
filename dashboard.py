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


def generate_gauge_chart(column_name, title, width, height):
    value = student_data[column_name].values[0]  # Get the value for the specific activity
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    fig.update_layout(width=width, height=height)
    with st.container():
        st.plotly_chart(fig)


def create_tabs(data, page, info):

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
        id_student, full_name, id_career, id_course, time_taken = st.columns(5)

        with id_student:
            st.subheader("**MATRICULA** ", anchor=False)
            st.write(f"{selected_student_data['matricula'].values[0]}")
        with full_name:
            st.subheader("**ESTUDIANTE**", anchor=False)
            st.write(f"{selected_student_data['nombre_completo'].values[0]}")
        with id_career:
            st.subheader("**ID CARRERA**", anchor=False)
            st.write(f"{selected_student_data['carrera'].values[0]}")
        with id_course:
            st.subheader("**PARALELO**", anchor=False)
            st.write(f"{selected_student_data['paralelo'].values[0]}")
        with time_taken:
            st.subheader("**VEZ TOMADA**", anchor=False)
            st.write(f"{selected_student_data['vez_tomada'].values[0]}")
        st.markdown("""
                       <style>
                           .e1nzilvr5 p{
                                   text-align: center;
    
                       }
                   </style>
                   """, unsafe_allow_html=True)
        with st.container():
            year, period, teacher, status = st.columns(4, gap="small")
            with year:
                st.subheader("**AÑO**", anchor=False)
                st.write(f"{selected_student_data['anio'].values[0]}")
            with period:
                st.subheader("**PERIODO**", anchor=False)
                st.write(f"{selected_student_data['periodo'].values[0]}")
            with teacher:
                st.subheader("**PROFESOR**", anchor=False)
                st.write(f"{selected_student_data['profesor'].values[0]}")
            with status:
                st.subheader("**ESTADO**", anchor=False)
                st.write(f"{selected_student_data['estado'].values[0]}")
        st.write("---")

        with st.container():
            st.subheader("Notas Obtenidas", anchor=False)
            theoretical, practice = st.columns(2)
            with theoretical:
                generate_gauge_chart('nota_teorico', 'Nota Teórica', 450, 350)
            with practice:
                generate_gauge_chart('nota_practico', 'Nota Practico', 450, 350)
        st.write("---")

        with st.container():
            st.header("Lecciones", anchor=False)
            l_1, l_2, l_3, l_4 = st.columns(4)
            with l_1:
                generate_gauge_chart('leccion_1', '# 1', 200, 350)
            with l_2:
                generate_gauge_chart('leccion_2', '# 2', 200, 350)
            with l_3:
                generate_gauge_chart('leccion_3', '# 3', 200, 350)
            with l_4:
                generate_gauge_chart('leccion_4', '# 4', 200, 350)
        st.write("---")
        with st.container():
            st.header("Talleres", anchor=False)
            w_1, w_2, w_3, w_4 = st.columns(4)
            with w_1:
                generate_gauge_chart('taller_1', '# 1', 200, 350)
            with w_2:
                generate_gauge_chart('taller_2', '# 2', 200, 350)
            with w_3:
                generate_gauge_chart('taller_3', '# 3', 200, 350)
            with w_4:
                generate_gauge_chart('taller_4', '# 4', 200, 350)
        st.write("---")
        with st.container():
            st.header("Examenes", anchor=False)
            e_p, e_f, e_m = st.columns(3)
            with e_p:
                generate_gauge_chart('examen_parcial', '# 1', 200, 350)
            with e_f:
                generate_gauge_chart('examen_final', '# 2', 200, 350)
            with e_m:
                generate_gauge_chart('examen_mejoramiento', '# 3', 200, 350)

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


def comparative_graphs(columns, data, title):
    with st.container():
        st.markdown(f"""
                    <div font-size: 50px;>
                    <span>{title.upper()}</span>
                    </div>
                    """, unsafe_allow_html=True)
        fig = go.Figure()
        grouped = data.groupby('anio')

        for year, group in grouped:
            fig.add_trace(
                go.Scatter(
                    x=columns,
                    y=group[columns].mean(),
                    name=str(year),
                    mode='lines+markers'
                )
            )
        name_columns = []
        for col in columns:
            name_columns.append(col.replace("_", " ").upper())
        # Configura el diseño del gráfico
        fig.update_layout(
            title=f'Puntajes por {title.capitalize()} en Diferentes Periodos',
            xaxis_title=title.upper(),
            yaxis_title='Puntaje Promedio',
            xaxis=dict(tickvals=[0, 1, 2, 3], ticktext=name_columns),
            legend=dict(title='Año'),
        )

        # Muestra el gráfico
        st.plotly_chart(fig)


dashboard = st.empty()
dashboard.title("Performance Review Programming Fundamentals", anchor=False)
dashboard.write("Upload Actual Performance CSV",)
actual_file = dashboard.file_uploader("actual_performance", ["csv"],
                                      accept_multiple_files=False, key="actual_performance", label_visibility="hidden")

if actual_file is not None:
    dashboard.empty()
    dataframe = pd.read_csv(actual_file)
    st.title("Programming Fundamentals Review".upper(), anchor=False)

    selected_student = None

    with st.sidebar.container():
        selected_student = st.selectbox("Choose a student:", dataframe["nombre_completo"].unique())
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
    student_data = dataframe[dataframe.nombre_completo == selected_student].fillna(0)
    student_data["estado"] = student_data.apply(
        lambda x: "AP" if((x.nota_teorico*0.7)+(x.nota_practico*0.3)) > 60 else "RP", axis=1)
    student_data = student_data.sort_values(by="anio", ascending=False).reset_index(drop=True)
    st.markdown("""
        <div font-size: 200px;>
            <span>STUDENT INFORMATION</span>
        </div>
    """, unsafe_allow_html=True)
    years_period = [f"{str(row.anio)}-{row.periodo}" for idx, row in student_data.iterrows()]
    years_period.append("COMPARATIVA")
    tabs = st.tabs(years_period)
    for tab in tabs[:-1]:
        with tab:
            create_tabs(student_data, tab, years_period[tabs.index(tab)])

    with tabs[-1]:
        lesson_columns = ['leccion_1', 'leccion_2', 'leccion_3', 'leccion_4']
        exam_columns = ['examen_parcial', 'examen_final', 'examen_mejoramiento']
        workshop_columns = ['taller_1', 'taller_2', 'taller_3', 'taller_4']

        comparative_graphs(lesson_columns, student_data, "Lecciones")
        comparative_graphs(workshop_columns, student_data, "Talleres")
        comparative_graphs(exam_columns, student_data, "Exámenes")
