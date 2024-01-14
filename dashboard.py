from functions.graph_fun import *

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
                generate_gauge_chart_without_steps(selected_student_data, "nota_teorico", "Nota Teórica", 450, 350)
            with practice:
                generate_gauge_chart_without_steps(selected_student_data, "nota_practico", "Nota Practico", 450, 350)
        st.write("---")

        act_values = list(columns.values())[1:]
        for value in range(3):
            create_graph_per_activity_wos(selected_student_data, columns["titles"][value + 1], act_values[value])

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


dashboard = st.empty()
dashboard.title("Performance Review Programming Fundamentals", anchor=False)
dashboard.write("Upload Actual Performance CSV",)
actual_file = dashboard.file_uploader("actual_performance", ["csv"],
                                      accept_multiple_files=False, key="actual_performance", label_visibility="hidden")
comparative_categories = ["Consigo mismo", "Veces Tomada", "Paralelo", "Carrera", "Tipo", "Novatos", "Todos"]
if actual_file is not None:
    dashboard.empty()
    dataframe = pd.read_csv(actual_file, sep=";")
    st.title("Programming Fundamentals Review".upper(), anchor=False)

    if "selected_comparative" not in st.session_state:
        st.session_state.selected_comparative = comparative_categories[0]

    def on_select_student_change():
        st.session_state.selected_comparative = comparative_categories[0]

    with st.sidebar.container():
        selected_student = st.selectbox("Elija un estudiante:", dataframe["estudiante"].unique(),
                                        on_change=on_select_student_change)
        selected_comparative = st.selectbox("Elija una comparativa", comparative_categories, key="selected_comparative")

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
    student_data = get_student_dataframe(dataframe, selected_student)
    activities = {"notes": ["nota_teorico", "nota_practico"],
                  "lesson_columns": ["leccion_1", "leccion_2", "leccion_3", "leccion_4"],
                  "exam_columns": ["examen_parcial", "examen_final", "examen_mejoramiento"],
                  "workshop_columns": ["taller_1", "taller_2", "taller_3", "taller_4"],
                  "titles": ["Notas", "Lecciones", "Talleres", "Exámenes"]
                  }
    st.markdown("""
        <div font-size: 200px;>
            <span>STUDENT INFORMATION</span>
        </div>
    """, unsafe_allow_html=True)
    years_period = [f"{str(row.anio)}-{row.periodo}" for idx, row in student_data.iterrows()]
    student_data["year_period"] = years_period
    years_period = sorted(years_period, key=obtain_year_period, reverse=True)
    years_period.append(f"COMPARATIVA {selected_comparative.upper()}")
    tabs = st.tabs(years_period)
    
    for tab in tabs[:-1]:
        with tab:
            create_tabs(student_data, tab, years_period[tabs.index(tab)], activities)

    with tabs[-1]:
        comparative_graphs(dataframe, activities, student_data,  selected_comparative, comparative_categories)
