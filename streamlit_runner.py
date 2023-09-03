from subprocess import Popen
import time

Popen(
    "streamlit run program\\streamlit\\streamlit_app_portfolio.py --server.headless true --server.baseUrlPath strategy_tester --server.runOnSave false --theme.base dark",
    shell=True)

while True:
    time.sleep(0.1)