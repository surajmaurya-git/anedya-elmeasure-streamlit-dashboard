import streamlit as st
import streamviz as sv
from datetime import datetime
import pytz
import numpy as np
import pandas as pd
import time
import json
import time
from components.charts import draw_chart

def unit_header(title, des=None, node_client=None,device_status_res=None):
    if title is None:
        st.error("Please provide a valid title.")
    VARIABLES= st.session_state.variables
    headercols = st.columns([1,0.11,0.11, 0.11], gap="small")
    with headercols[0]:
        st.title(title, anchor=False)
    with headercols[1]:
        if device_status_res is not None or device_status_res.get("status") is True:
            device_status=None
            if device_status_res.get("device_status"):
                device_status="Online"
            else:
                device_status="Offline"
        else:
            device_status="..."
        st.button(device_status,disabled=True,use_container_width=True)
    with headercols[2]:
        on = st.button("Refresh")
        if on:
            st.rerun()
    with headercols[3]:
        logout = st.button("Logout")
        if logout:
            st.session_state.LoggedIn = False
            st.rerun()
    if des is not None:
        st.markdown(des)

def unit_details(data):
    # res=node_client.get_valueStore(key="DEVICEINFO")
    # st.write(res)
    # res_json=json.loads(res)
    # st.write(data)
    st.markdown(f"**Node ID:** {data}")
    # st.markdown(f"**Firmware:**  ")
    # st.text(f"IMEI No.: {data.get('imei_id')}")


def cards_section(data:dict=None):
    container = st.container(border=True)
    with container:
        st.subheader(body="Parameters", anchor=False)
        r1_cols = st.columns([1,1,1,1], gap="small")
        with r1_cols[0]:
            BOOKING_STATUS=data.get("booking")
            value="ND"
            if BOOKING_STATUS:
                value="Booked"
            else:
                value="Not Booked"
            st.metric(label="Booking Status", value=value,border=True)
        with r1_cols[1]:
            TIME_LEFT=data.get("timeLeft")
            st.metric(label="Time Left", value=TIME_LEFT,border=True)
        with r1_cols[2]:
            END_EPOCH=data.get("endEpoch")
            st.metric(label="End Epoch", value=END_EPOCH,border=True)
        with r1_cols[3]:
            NAP_TIME=data.get("napTime")
            st.metric(label="Nap Time", value=NAP_TIME,border=True)
        
        r2_cols = st.columns([1,1,1,1], gap="small")
        with r2_cols[0]:
            WIFI_SIGNAL=data.get("wifiSignal")
            st.metric(label="Wifi Signal", value=WIFI_SIGNAL,border=True)

        with r2_cols[1]:
            RFID_GAIN=data.get("rfidGain")
            st.metric(label="RFID Gain", value=RFID_GAIN,border=True)

        with r2_cols[2]:
            RFID=data.get("rfid")
            st.metric(label="RFID", value=RFID,border=True)
        with r2_cols[3]:
            CAN=data.get("can")
            st.metric(label="CAN", value=CAN,border=True)



def gauge_section(node_client=None):
    container = st.container(border=True,height=300)
    VARIABLES= st.session_state.variables
    with container:

        indian_time_zone = pytz.timezone('Asia/Kolkata')   # set time zone
        r1_guage_cols = st.columns([1,1,1], gap="small")
        
        with r1_guage_cols[0]:
            VARIABLE=VARIABLES["variable_1"]
            data=node_client.get_latestData(VARIABLE["identifier"])
            if data.get("data") != None:
                timestamp=data.get("timestamp")
                hr_timestamp = datetime.fromtimestamp(timestamp, indian_time_zone)
                fm_hr_timestamp=hr_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')
                st.markdown(f"**Last Updated:** {fm_hr_timestamp}")
                value=data.get("data")
                sv.gauge(value,"Frequency",cWidth=True,gSize="MED",sFix=VARIABLE["unit"],arTop=int(VARIABLE["top_range"]),arBot=int(VARIABLE["bottom_range"]))
            else:
                st.error("No Data Available")
        with r1_guage_cols[1]:
            VARIABLE=VARIABLES["variable_2"]
            data=node_client.get_latestData(VARIABLE["identifier"])
            if data.get("data") != None:
                timestamp=data.get("timestamp")
                hr_timestamp = datetime.fromtimestamp(timestamp, indian_time_zone)
                fm_hr_timestamp=hr_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')
                st.markdown(f"**Last Updated:**  {fm_hr_timestamp}")
                value=data.get("data")
                arTop=int(VARIABLE["top_range"])
                arBot=int(VARIABLE["bottom_range"])
                sv.gauge(value,VARIABLE["name"],cWidth=True,gSize="MED",sFix="V",arTop=arTop,arBot=arBot)
            else:
                st.error("No Data Available")
        with r1_guage_cols[2]:
            VARIABLE=VARIABLES["variable_5"]
            data=node_client.get_latestData(VARIABLE["identifier"])
            if data.get("data") != None:
                timestamp=data.get("timestamp")
                hr_timestamp = datetime.fromtimestamp(timestamp, indian_time_zone)
                fm_hr_timestamp=hr_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')
                st.markdown(f"**Last Updated:**  {fm_hr_timestamp}")
                value=data.get("data")
                arTop=int(VARIABLE["top_range"])
                arBot=int(VARIABLE["bottom_range"])
                sv.gauge(value,VARIABLE["name"],cWidth=True,gSize="MED",sFix=VARIABLE["unit"],arTop=arTop,arBot=arBot)
            else:
                st.error("No Data Available")

def sync_controllers_state(node_client=None):
    
    res = node_client.get_valueStore(key="door")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 0:
            st.session_state.door = "Open Door"
        elif(value == 1):
            st.session_state.door = "Close Door"
        else:
            print("Invalid value")

    res = node_client.get_valueStore(key="light")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 0:
            st.session_state.light = "Turn Light On"
        elif(value <= 5):
            st.session_state.light = "Turn Light Off"
        else:
            print("Invalid value")

    res = node_client.get_valueStore(key="fan")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 1:
            st.session_state.fan = "Turn Fan Off"
        elif(value <= 3):
            st.session_state.fan = "Turn Fan On"

    res = node_client.get_valueStore(key="massage")
    if res.get("isSuccess") is True and res.get("value") is not None:
        value = res.get("value")
        if value == 1:
            st.session_state.massage = "Turn Massager Off"
        else:
            st.session_state.massage = "Turn Massager On"

def controllers_section(node_client=None):
    if node_client is None:
        st.stop()
    container = st.container(border=True)
    with container:
        st.subheader(body="Controllers", anchor=False)
        sync_controllers_state(node_client=node_client)
        r1_cols = st.columns([1,1,1,1], gap="small")
        with r1_cols[0]:
            st.subheader("Door")
            state = st.button(st.session_state.door,key="door_key")
            if state:
                if st.session_state.door== "Open Door":
                    st.session_state.door = "Close Door"
                    node_client.set_valueStore(key="door", value=1,type="float")
                else:
                    st.session_state.door = "Open Door"
                    node_client.set_valueStore(key="door", value=0,type="float")
                st.rerun()
        with r1_cols[1]:
            st.subheader("Light")
            state = st.button(st.session_state.light,key="light_toggle")
            if state:
                if st.session_state.light== "Turn Light On":
                    st.session_state.light = "Turn Light Off"
                    node_client.set_valueStore(key="light", value=1,type="float")
                else:
                    st.session_state.light = "Turn Light On"
                    node_client.set_valueStore(key="light", value=0,type="float")
                st.rerun()
        with r1_cols[2]:
            st.subheader("Fan")
            state = st.button(st.session_state.fan,key="fan_toggle")
            if state:
                if st.session_state.fan== "Turn Fan On":
                    st.session_state.fan = "Turn Fan Off"
                    node_client.set_valueStore(key="fan", value=1,type="float")
                else:
                    st.session_state.fan = "Turn Fan On"
                    node_client.set_valueStore(key="fan", value=0,type="float")
                st.rerun()
        with r1_cols[3]:
            st.subheader("Massager")
            state = st.button(st.session_state.massage,key="massage_toggle")
            if state:
                if st.session_state.massage== "Turn Massager On":
                    st.session_state.massage = "Turn Massager Off"
                    node_client.set_valueStore(key="massage", value=1,type="float")
                else:
                    st.session_state.massage = "Turn Massager On"
                    node_client.set_valueStore(key="massage", value=0,type="float")
                st.rerun()

def graph_section(node_client=None):
    if node_client is None:
        st.stop()
    container = st.container(border=True)
    with container:
        st.subheader(body="Visualizations", anchor=False)
        currentTime = int(time.time())    #to means recent time
        pastHour_Time = int(currentTime - 86400)

        VARIABLES=st.session_state.variables
        options:list=[]
        user_variables_access = st.session_state.user_variables_access
        if st.session_state.view_role == "user":
            for key, variable in VARIABLES.items():
                variable_name = variable.get('name')
                if variable_name in user_variables_access:
                    options.append(variable_name)
        else:
            for key, variable in VARIABLES.items():
                variable_name = variable.get('name')
                options.append(variable_name)

        # st.write(VARIABLES)

        multislect_cols = st.columns([0.7,1], gap="small")
        with multislect_cols[0]:
            show_charts=st.multiselect("Show Charts",placeholder="Show Charts",options=options,label_visibility="hidden")


        for i in range(0, len(show_charts), 3):
            graph_cols = st.columns([1, 1, 1], gap="small")
            for j, chart in enumerate(show_charts[i:i+3]):
                with graph_cols[j]:
                    VARIABLE_KEY = get_variable_key_by_name(VARIABLES, chart)
                    if VARIABLE_KEY is not None:
                        VARIABLE = VARIABLES.get(VARIABLE_KEY)
                        data = node_client.get_data(VARIABLE.get("identifier"), pastHour_Time, currentTime)
                        draw_chart(chart_title=chart, chart_data=data, y_axis_title=VARIABLE.get("unit"), bottomRange=VARIABLE.get("bottom_range"), topRange=VARIABLE.get("top_range"))
                    else:
                        st.subheader(chart)
                        st.error("Variable not found")

def map_section(node_client=None):
    container = st.container(border=True)
    with container:
        st.subheader(body="Device Location", anchor=False)
        res=node_client.get_latestData("location")
        if res.get("data") is not None:
            location=res.get("data")
            last_updated=res.get("timestamp")
            indian_time_zone = pytz.timezone('Asia/Kolkata')   # set time zone
            hr_timestamp = datetime.fromtimestamp(last_updated, indian_time_zone)
            fm_hr_timestamp=hr_timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')
            st.markdown(f"**Last Updated:**  {fm_hr_timestamp}")

            latitude=location.get("lat")
            longitude=location.get("long")  
            locationData = pd.DataFrame(
                {"latitude": [latitude], "longitude": [longitude]}
            )
            st.map(
                locationData, zoom=13, color="#0044ff", size=50, use_container_width=True
            )
        else:
            st.error("No Data Available")

def get_variable_key_by_name(data, search_name):
    for key, variable in data.items():
        if variable["name"] == search_name:
            return key
    return None

