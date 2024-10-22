import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import mysql.connector
import time

title = st.title('Red Bus')
subtitle = st.markdown('Online Bus Ticket Booking Site')

andhra = pd.read_csv("all_data_ap.csv")["Route_name"].tolist()
kerala = pd.read_csv("all_data_k.csv")["Route_name"].tolist()
telungana = pd.read_csv("all_data_t.csv")["Route_name"].tolist()
kadamba = pd.read_csv("all_data_kad.csv")["Route_name"].tolist()
rajasthan = pd.read_csv("all_data_r.csv")["Route_name"].tolist()
sb = pd.read_csv("all_data_sb.csv")["Route_name"].tolist()
hp = pd.read_csv("all_data_hp.csv")["Route_name"].tolist()
assam = pd.read_csv("all_data_a.csv")["Route_name"].tolist()
up = pd.read_csv("all_data_up.csv")["Route_name"].tolist()
bihar = pd.read_csv("all_data_b.csv")["Route_name"].tolist()

web = option_menu(menu_title="Online Bus",
                  options=["Home", "States and Routes"],
                  icons=["house", "info-circle"],
                  orientation="horizontal")

if web == "Home":
    st.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")

if web == "States and Routes":
    col1, col2 = st.columns(2)
    with col1:
        state = st.selectbox("List of States", ['Andhra Pradesh', 'Kerala', 'Telungana', 'Kadamba', 'Rajasthan', 
                                                'South Bengal', 'Himachal Pradesh', 'Assam', 'Uttar Pradesh', 'Bihar'])
    with col2:
        select_type = st.selectbox("Choose bus type", ["A/C", "NON A/C", "sleeper", "semi-sleeper", "seater", "others"])
    
    with col1:
        fare_range = st.number_input("Enter fare", min_value=50, max_value=4000, value=50, step=50)
    with col2:
        select_rating = st.slider("Choose rating", min_value=1, max_value=5, value=5, step=1)
    with col1:
        TIME = st.time_input("Select the time")
        time_str = TIME.strftime("%H:%M:%S")

    if state == "Andhra Pradesh":
        with col2:
            A = st.selectbox("List of routes", andhra)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, A, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Kerala":
        with col2:
            K = st.selectbox("List of routes", kerala)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, K, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Telungana":
        with col2:
            T = st.selectbox("List of routes", telungana)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, T, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Kadamba":
        with col2:
            K = st.selectbox("List of routes", kadamba)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, K, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Rajasthan":
        with col2:
            R = st.selectbox("List of routes", rajasthan)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, R, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "South Bengal":
        with col2:
            SB = st.selectbox("List of routes", sb)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, SB, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Himachal Pradesh":
        with col2:
            H = st.selectbox("List of routes", hp)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, H, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Assam":
        with col2:
            A = st.selectbox("List of routes", assam)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, A, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Uttar Pradesh":
        with col2:
            UP = st.selectbox("List of routes", up)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, UP, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)

    if state == "Bihar":
        with col2:
            B = st.selectbox("List of routes", bihar)

        def type_and_fare(bus_type, fare_range, rate_range):
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="181506",
                    database="redbus",
                    port="3306"
                )
                mycursor = mydb.cursor()
                rate_min, rate_max = 0, 5  
                if rate_range == 5:
                    rate_min, rate_max = 4.2, 5
                elif rate_range == 4:
                    rate_min, rate_max = 3.0, 4.2
                elif rate_range == 3:
                    rate_min, rate_max = 2.0, 3.0
                elif rate_range == 2:
                    rate_min, rate_max = 1.0, 2.0
                elif rate_range == 1:
                    rate_min, rate_max = 0, 1.0

                bus_type_option = {
                    "sleeper": "bus_type LIKE '%Sleeper%'",
                    "semi-sleeper": "bus_type LIKE '%Semi Sleeper%'",
                    "A/C": "bus_type LIKE '%A/C%'",
                    "NON A/C": "bus_type LIKE '%NON A/C%'",
                    "seater": "bus_type LIKE '%Seater%'",
                    "others": (
                        "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%' "
                        "AND bus_type NOT LIKE '%Seater%' AND bus_type NOT LIKE '%A/C%' "
                        "AND bus_type NOT LIKE '%NON A/C%'"
                    )
                }.get(bus_type, "bus_type LIKE '%%'")

                query = f"""
                    SELECT * FROM redbusdetails
                    WHERE price <= %s
                    AND route_name = %s
                    AND {bus_type_option}
                    AND departing_time >= %s
                    AND star_rating BETWEEN %s AND %s
                    ORDER BY price, departing_time DESC
                """
                mycursor.execute(query, (fare_range, B, time_str, rate_min, rate_max))
                out = mycursor.fetchall()
                mydb.close()

                df = pd.DataFrame(out, columns=["ID", "Route_name", "Route_link", "Bus_name", "Bus_type","Departing_time", "Duration", "Reaching_time","Star_rating", "Price", "Seat_availability"])
                st.write(df)
                return df
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
                return pd.DataFrame()

        df_result = type_and_fare(select_type, fare_range, select_rating)










































    