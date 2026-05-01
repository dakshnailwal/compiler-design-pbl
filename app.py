# app.py

import streamlit as st

from lexer import tokenize
from parser import Parser
from semantic import SemanticAnalyzer
from intermediate_code import TACGenerator

st.set_page_config(page_title="Mini Compiler", layout="wide")

# -----------------------------
# DARK UI
# -----------------------------
st.markdown("""
<style>

.stApp { background-color: #0D1117; }

html, body, [class*="css"] {
    color: #FFFFFF !important;
    font-family: Consolas, monospace;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

h1 { color: #FFFFFF !important; }
h2 { color: #58A6FF !important; }
h3 { color: #FFFFFF !important; }

.stTabs [role="tab"] {
    color: #AAAAAA !important;
}

.stTabs [aria-selected="true"] {
    color: #00FFAA !important;
    border-bottom: 2px solid #00FFAA;
}

textarea {
    background-color: #161B22 !important;
    color: #00FFAA !important;
    border: 2px solid #58A6FF !important;
    caret-color: #FFCC00 !important;
}

.stButton>button {
    background-color: #238636;
    color: white;
    font-weight: bold;
}

table {
    border-collapse: collapse;
    margin: auto;
}

th {
    background-color: #161B22;
    color: #58A6FF;
    padding: 8px;
    text-align: left;
}

td {
    border-bottom: 1px solid #30363D;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1 style='text-align:center;'>Mini Compiler For Simple Arithmetic Language</h1>", unsafe_allow_html=True)

# -----------------------------
# INPUT
# -----------------------------
st.markdown("<h3 style='margin-bottom:0px;'>Enter your program:</h3>", unsafe_allow_html=True)
code = st.text_area("", height=200, label_visibility="collapsed")

# -----------------------------
# COMPILE
# -----------------------------
if st.button("Compile"):

    try:
        tokens = tokenize(code)

        parser = Parser(tokens)
        parser.parse_program()

        semantic = SemanticAnalyzer(tokens)
        semantic.analyze()

        tac = TACGenerator(tokens)
        code_lines = tac.generate()

        st.success("Syntax: No errors found")

        tab1, tab2, tab3 = st.tabs(["Tokens", "Symbol Table", "Intermediate Code"])

        # -----------------------------
        # TOKENS
        # -----------------------------
        with tab1:
            st.markdown("### 🔹 Tokens")

            rows = ""
            for t in tokens:
                rows += (
                    f"<tr>"
                    f"<td style='color:#00FFAA;padding-right:40px;'>{t.value}</td>"
                    f"<td style='color:#E6EDF3;'>{t.type}</td>"
                    f"</tr>"
                )

            table = (
                "<table style='width:420px;'>"
                "<thead><tr>"
                "<th>Value</th>"
                "<th>Type</th>"
                "</tr></thead><tbody>"
                + rows +
                "</tbody></table>"
            )

            st.markdown(table, unsafe_allow_html=True)

        # -----------------------------
        # SYMBOL TABLE
        # -----------------------------
        with tab2:
            st.markdown("### 🔹 Symbol Table")

            rows = ""
            for var, info in semantic.symbol_table.table.items():
                rows += (
                    f"<tr>"
                    f"<td style='color:#00FFAA;padding-right:40px;'>{var}</td>"
                    f"<td style='color:#E6EDF3;'>{info['type']}</td>"
                    f"</tr>"
                )

            table = (
                "<table style='width:420px;'>"
                "<thead><tr>"
                "<th>Variable</th>"
                "<th>Type</th>"
                "</tr></thead><tbody>"
                + rows +
                "</tbody></table>"
            )

            st.markdown(table, unsafe_allow_html=True)

        # -----------------------------
        # INTERMEDIATE CODE
        # -----------------------------
        with tab3:
            st.markdown("### 🔹 Intermediate Code")

            for line in code_lines:
                st.markdown(
                    f"<div style='background:#161B22;padding:10px;border-radius:6px;margin-bottom:6px;color:#00FFAA'>{line}</div>",
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(str(e))