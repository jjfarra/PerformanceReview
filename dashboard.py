import streamlit as st
import pandas as pd
import numpy
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
        selected_student = st.selectbox("Choose a student:", dataframe["nombre_completo"])
    student_data = dataframe[dataframe.nombre_completo == selected_student]

    st.markdown("""
        <div font-size: 20px;>
            <span>STUDENT INFORMATION</span>
        </div>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown("""
            <style>
                div[data-testid="column"] h3 {
                        text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)

        st.write("---")
        id_student, full_name, id_career, id_course, time_taken = st.columns(5)

        with id_student:
            st.subheader("**MATRICULA** ", anchor=False)
            st.write(f"{student_data['matricula'].values[0]}")
        with full_name:
            st.subheader("**ESTUDIANTE**", anchor=False)
            st.write(f"{student_data['nombre_completo'].values[0]}")
        with id_career:
            st.subheader("**ID CARRERA**", anchor=False)
            st.write(f"{student_data['carrera'].values[0]}")
        with id_course:
            st.subheader("**PARALELO ACTUAL**", anchor=False)
            st.write(f"{student_data['paralelo_actual'].values[0]}")
        with time_taken:
            st.subheader("**VEZ TOMADA**", anchor=False)
            st.write(f"{student_data['vez_tomada'].values[0]}")
        st.markdown("""
                       <style>
                           .e1nzilvr5 p{
                                   text-align: center;

                       }
                   </style>
                   """, unsafe_allow_html=True)
        st.write("---")

    with st.container():
        st.subheader("Notas Obtenidas", anchor=False)
        teorical, practice = st.columns(2)
        with teorical:
            generate_gauge_chart('nota_teorico', 'Nota Teórica', 450, 350)
        with practice:
            generate_gauge_chart('nota_practico', 'Nota Practico', 450, 350)
    st.write("---")

    with st.container():
        lessons, workshops = st.columns(2, gap="small")

        with lessons:
            st.header("Lecciones", anchor=False)
            l_1, l_2, l_3, l_4 = st.columns(4)
            with l_1:
                generate_gauge_chart('leccion_1', '# 1', 150, 350)
            with l_2:
                generate_gauge_chart('leccion_2', '# 2', 150, 350)
            with l_3:
                generate_gauge_chart('leccion_3', '# 3', 150, 350)
            with l_4:
                generate_gauge_chart('leccion_4', '# 4', 150, 350)
        st.markdown("""<hr style="width: 3px; height: 300px; border: 0;
         background-color: black;">""", unsafe_allow_html=True)

        with workshops:
            st.header("Talleres", anchor=False)
            w_1, w_2, w_3, w_4 = st.columns(4)
            with w_1:
                generate_gauge_chart('taller_1', '# 1', 150, 350)
            with w_2:
                generate_gauge_chart('taller_2', '# 2', 150, 350)
            with w_3:
                generate_gauge_chart('taller_3', '# 3', 150, 350)
            with w_4:
                generate_gauge_chart('taller_4', '# 4', 150, 350)

        st.markdown("""
           <style>
               .e1nzilvr1 {
                       text-align: center;
           }
            </style>
       """, unsafe_allow_html=True)