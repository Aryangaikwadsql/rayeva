"""Streamlit demo UI with loading spinner."""

import streamlit as st
import requests
import time


st.title("🟢 Rayeva AI Systems Demo")

st.header("Module 1: AI Category Generator")
product_desc = st.text_area("Product description", "Eco-friendly bamboo toothbrush")

if st.button("Generate Category", type="primary"):
    with st.spinner("Generating category with AI..."):
        try:
            resp = requests.post(
                "http://localhost:8000/ai/category", 
                json={"product_desc": product_desc},
                timeout=30  # Prevent infinite hang
            )
            if resp.status_code == 200:
                st.success("✅ Category generated!")
                st.json(resp.json())
            else:
                st.error(f"❌ Error {resp.status_code}: {resp.text}")
        except requests.exceptions.Timeout:
            st.error("⏰ Request timeout - check if server running on localhost:8000")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to server - run `python run.py` first")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

st.header("Module 2: AI Proposal Generator")
client_needs = st.text_area("Client needs", "Sustainable office supplies for 50 employees")
budget = st.number_input("Budget ($)", value=5000.0, min_value=0.0)

if st.button("Generate Proposal", type="secondary"):
    with st.spinner("Generating proposal with AI..."):
        try:
            resp = requests.post(
                "http://localhost:8000/ai/proposal", 
                json={"client_needs": client_needs, "budget": budget},
                timeout=30
            )
            if resp.status_code == 200:
                st.success("✅ Proposal generated!")
                st.json(resp.json())
            else:
                st.error(f"❌ Error {resp.status_code}: {resp.text}")
        except requests.exceptions.Timeout:
            st.error("⏰ Request timeout - check server")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Server not running - start with `python run.py`")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

st.header("Module 3: AI Impact Report")
product_id = st.number_input("Product ID", value=1)
proposal_id = st.number_input("Proposal ID", value=1)
if st.button("Generate Impact", type="primary"):
    resp = requests.post("http://localhost:8000/ai/impact", json={"product_id": product_id, "proposal_id": proposal_id}, timeout=30)
    if resp.status_code == 200:
        st.json(resp.json())
    else:
        st.error(resp.text)

st.header("Module 4: WhatsApp Bot")
whatsapp_msg = st.text_input("Message", "order status")
phone = st.text_input("Phone", "+123456")
if st.button("Send WhatsApp"):
    resp = requests.post("http://localhost:8000/ai/whatsapp", json={"message": whatsapp_msg, "phone": phone}, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        st.success(data.get("response", data))  # Handle direct response or dict

