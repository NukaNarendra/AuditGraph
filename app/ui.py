import streamlit as st
import sys
import os

# Add root to path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator.langgraph_bot import audit_bot
from langchain_core.messages import HumanMessage
from src.graph.neo4j_client import Neo4jClient

st.set_page_config(page_title="AuditGraph AI", layout="wide")

st.title("🕵️ AuditGraph: Autonomous Due Diligence")

# Sidebar for controls
with st.sidebar:
    st.header("Control Panel")
    if st.button("Reset Database Connection"):
        st.cache_resource.clear()
        st.success("Connection reset!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Layout: Split screen (Chat vs. Live Data)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💬 Audit Assistant")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask the auditor (e.g., 'Check for hidden debt')"):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. AI Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🔍 *Auditing...*")

            # Run LangGraph Agent
            try:
                inputs = {"messages": [HumanMessage(content=prompt)]}
                result = audit_bot.invoke(inputs)

                # Extract the final response text
                bot_response = result['messages'][-1].content

                message_placeholder.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"Error: {e}")

with col2:
    st.subheader("📊 Live Graph Evidence")

    # Simple view of suspicious nodes from Neo4j
    client = Neo4jClient()
    st.markdown("**Latest Suspicious Transactions:**")

    try:
        # Query for high-risk money flows
        query = """
        MATCH (a)-[r:TRANSFERRED_MONEY]->(b)
        WHERE r.amount > 10000 
        RETURN a.id as Sender, b.id as Receiver, r.amount as Amount
        LIMIT 10
        """
        data = client.query(query)
        if data:
            st.dataframe(data)
        else:
            st.info("No suspicious transactions found yet.")
    except Exception as e:
        st.warning("Database not connected yet.")

    client.close()