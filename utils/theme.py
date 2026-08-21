import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

        /* Global Typography and Colors */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #0f172a !important; /* Dark text */
        }

        /* Capitalize Headers & Titles */
        h1, h2, h3, h4, h5, h6, .st-emotion-cache-10trblm, [data-testid="stHeader"] {
            font-family: 'Hanken Grotesk', sans-serif !important;
            color: #0f172a !important;
            text-transform: capitalize !important;
        }

        h1 {
            font-weight: 800 !important;
            letter-spacing: -0.02em;
        }

        /* Aggressive styling of Streamlit Metrics to look like product cards */
        [data-testid="stMetric"] {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        }

        [data-testid="stMetricLabel"] {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            color: #64748b !important;
            text-transform: capitalize !important;
        }

        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            font-size: 28px !important;
        }

        /* Info boxes */
        div.stInfo {
            background-color: #f0fdf4 !important; /* light green for info */
            border-left: 4px solid #22c55e !important;
            border-radius: 8px !important;
            color: #166534 !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }

        div.stInfo p {
            text-transform: capitalize !important;
        }

        /* Buttons - Modern SaaS style */
        div.stButton > button {
            background-color: #2563eb !important; /* Premium blue */
            color: #ffffff !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
            transition: all 0.2s ease !important;
            text-transform: capitalize !important;
        }

        div.stButton > button:hover {
            background-color: #1d4ed8 !important;
            box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.3);
            transform: translateY(-1px);
        }

        /* Input Fields */
        div.stTextInput > div > div > input {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
            color: #0f172a !important;
            padding: 0.75rem !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }

        div.stTextInput > div > div > input:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
        }

        /* Layout cleanup */
        .block-container {
            max-width: 1200px !important;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        /* Footer styling */
        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 14px;
            padding-top: 40px;
            font-weight: 500;
        }
        
        /* Subheaders to act like SaaS section headers */
        h3 {
            padding-bottom: 8px;
            border-bottom: 2px solid #f1f5f9;
            margin-bottom: 16px;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )
