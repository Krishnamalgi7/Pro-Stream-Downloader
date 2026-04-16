import os
import sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    # 1. Find the path to your app.py whether running as .exe or raw python
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    app_path = os.path.join(bundle_dir, 'app.py')

    # 2. Command Streamlit to run your app
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.headless=true",
        "--global.developmentMode=false"
    ]

    # 3. Execute
    sys.exit(stcli.main())