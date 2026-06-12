import streamlit as str_web
import pandas as pd
import json
import os

# Баптаулар
str_web.set_page_config(page_title="Кәсіби Бағдар", page_icon="🎓", layout="wide")

DB_FILE = "school_project_database.json"

# Деректер базасын жүктеу және сақтау
def load_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"users_db": {}, "teachers_db": {}}
    return {"users_db": {}, "teachers_db": {}}

def save_database(db_data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)

db = load_database()
if "users_db" not in str_web.session_state: str_web.session_state.users_db = db.get("users_db", {})
if "teachers_db" not in str_web.session_state: str_web.session_state.teachers_db = db.get("teachers_db", {})
if "current_user" not in str_web.session_state: str_web.session_state.current_user = None
if "current_teacher" not in str_web.session_state: str_web.session_state.current_teacher = None
if "step" not in str_web.session_state: str_web.session_state.step = 2

# Мамандықтар базасы
COMBINATION_INFO = {
    "Физика - Математика": {
        "бағыт": "ЖМБ",
        "грант_саны": "23,000+",
        "статистика": "IT және техникалық бағыт",
        "мамандықтар": ["Инженер", "Бағдарламашы", "Архитектор", "Математик"]
    },
    "Биология - Химия": {
        "бағыт": "ЖМБ",
        "грант_саны": "4,500+",
        "статистика": "Медициналық бағыт",
        "мамандықтар": ["Дәрігер", "Химик", "Фармацевт", "Биолог"]
    }
}

LIST_VIEW = ["Тегі", "Аты", "Сыныбы", "Орташа балл", "Комбинация"]

# Бүйірлік панель
user_role = str_web.sidebar.radio("Режим:", ["🎒 Оқушы бұрышы", "👩‍🏫 Мұғалімдер кеңсесі"])

# 1. ОҚУШЫ БӨЛІМІ
if user_role == "🎒 Оқушы бұрышы":
    if str_web.session_state.current_user is None:
        col1, col2 = str_web.columns(2)
        with col1:
            login_iin = str_web.text_input("ЖСН кіру:")
            pwd = str_web.text_input("Құпия сөз:", type="password")
            if str_web.button("Кіру"):
                if login_iin in str_web.session_state.users_db and str_web.session_state.users_db[login_iin]["password"] == pwd:
                    str_web.session_state.current_user = login_iin
                    str_web.rerun()
        with col2:
            reg_iin = str_web.text_input("Тіркелу ЖСН:")
            reg_pwd = str_web.text_input("Құпия сөз:", type="password")
            if str_web.button("Тіркелу"):
                str_web.session_state.users_db[reg_iin] = {"password": reg_pwd, "data": {}, "profile_done": False}
                save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
    else:
        user = str_web.session_state.users_db[str_web.session_state.current_user]
        str_web.write(f"Қош келдіңіз: {str_web.session_state.current_user}")
        if str_web.button("Шығу"):
            str_web.session_state.current_user = None
            str_web.rerun()

# 2. МҰҒАЛІМ БӨЛІМІ (Зигзаг алгоритмі)
elif user_role == "👩‍🏫 Мұғалімдер кеңсесі":
    if str_web.session_state.current_teacher is None:
        t_iin = str_web.text_input("Мұғалім ЖСН:")
        t_pwd = str_web.text_input("Құпия сөз:", type="password")
        if str_web.button("Кіру"):
            str_web.session_state.current_teacher = t_iin
            str_web.rerun()
    else:
        str_web.subheader("⚡ Зигзаг алгоритмі")
        students_data = [u["data"] for u in str_web.session_state.users_db.values() if "Комбинация" in u["data"]]
        if students_data:
            df = pd.DataFrame(students_data)
            if str_web.button("Сыныптарға бөлу"):
                for combo in COMBINATION_INFO.keys():
                    pool = df[df["Комбинация"] == combo].sort_values("Орташа балл", ascending=False).reset_index(drop=True)
                    a_class, ae_class = [], []
                    for idx, row in pool.iterrows():
                        if idx % 2 == 0: a_class.append(row)
                        else: ae_class.append(row)
                    
                    c1, c2 = str_web.columns(2)
                    c1.write(f"🏫 {combo} - 10 'А'"); c1.dataframe(pd.DataFrame(a_class)[LIST_VIEW])
                    c2.write(f"🏫 {combo} - 10 'Ә'"); c2.dataframe(pd.DataFrame(ae_class)[LIST_VIEW])
