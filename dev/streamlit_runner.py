from subprocess import Popen

Popen(
    "streamlit run streamlit_app_portfolio.py --server.headless true --server.baseUrlPath strategy_tester",
    shell=True)
