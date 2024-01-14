import streamlit as st
import plotly.graph_objects as go
from functions.data_fun import *


def generate_gauge_chart_without_steps(data, column_name, title, width, height):
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


def generate_gauge_chart_with_steps(data, column_name, title, c_factor, factor, mean, width, height):
    print(f"[{c_factor}] == {factor}")
    compare_value = data[data[c_factor] == factor][column_name].values[0]
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=compare_value,
        domain={"x": [0, 1], "y": [0, 1]},
        title={'text': title},
        delta={'reference': mean},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [{"range": [0, mean], "color": "lightgray"}],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": compare_value
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


def create_graph_per_activity_wos(data, title, columns):
    with st.container():
        st.header(title.capitalize(), anchor=False)
        cols = st.columns(len(columns))
        for idx in range(0, len(columns)):
            with cols[idx]:
                generate_gauge_chart_without_steps(data, columns[idx], f"# {idx+1}", 200, 350)

    st.write("---")


def create_graph_per_activity_ws(data, student_selected, title, columns, c_factor, function):
    with st.container():
        st.header(title.capitalize(), anchor=False)
        cols = st.columns(len(columns))
        for idx in range(0, len(columns)):
            times, mean_value = function(data, student_selected, columns[idx])
            with cols[idx]:
                generate_gauge_chart_with_steps(student_selected, columns[idx], f"# {idx+1}",
                                                c_factor, times, mean_value, 450, 350)

    st.write("---")


def self_comparative_graphs(columns, data, title):
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


def factor_compare_graph(activities, data, student_selected, c_factor, function):

    act_values = list(activities.values())[0:]
    for value in range(3):
        create_graph_per_activity_ws(data, student_selected,
                                     activities["titles"][value], act_values[value], c_factor, function)


def comparative_graphs(data, activities, selected_data, selected_comparative, comparative_categories):
    if selected_comparative == comparative_categories[0]:
        act_values = list(activities.values())[1:]
        for value in range(3):
            self_comparative_graphs(act_values[value], selected_data, activities["titles"][value + 1])
    elif selected_comparative == comparative_categories[1]:
        factor_compare_graph(activities, data, selected_data, "vez_tomada", get_times_taken_mean)
    elif selected_comparative == comparative_categories[2]:
        factor_compare_graph(activities, data, selected_data, "course", get_same_course)
    elif selected_comparative == comparative_categories[3]:
        factor_compare_graph(activities, data, selected_data, "carrera", get_same_career)
    elif selected_comparative == comparative_categories[5]:
        actual_year = int(dt.now().year)
        actual_month = int(dt.now().month)
        period = obtain_period(actual_year, actual_month)
        if period in selected_data.year_period and :
            factor_compare_graph(activities, data, selected_data, "year_period", get_novice)
        else:
            st.subheader(f"**NO ES NOVATO** ", anchor=False)