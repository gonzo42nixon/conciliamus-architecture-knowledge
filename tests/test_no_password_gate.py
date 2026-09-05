import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_PATHS = [
    os.path.join(ROOT_DIR, "app.py"),
    os.path.join(ROOT_DIR, "streamlit_app.py"),
]


def test_streamlit_apps_have_no_password_gate():
    for app_path in APP_PATHS:
        with open(app_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "check_password" not in content, f"Password gate still present in {app_path}"
        assert "APP_PASSWORD" not in content, f"APP_PASSWORD still referenced in {app_path}"
        assert "Geschützter Bereich" not in content, f"Login screen still present in {app_path}"
