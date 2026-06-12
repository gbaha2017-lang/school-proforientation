import streamlit as str_web  
import pandas as pd
import json
import os

# Баптаулар және ресми дизайн
str_web.set_page_config(page_title="Кәсіби Бағдар", page_icon="🎓", layout="wide")

# ==================== 💾 ФАЙЛДЫҚ БАЗАМЕН ЖҰМЫС (ДЕРЕКТЕР ӨШПЕЙДІ) ====================
DB_FILE = "school_project_database.json"

def load_database():
    """Файлдан мәліметтерді жүктеу, файл жоқ болса жаңа база құру"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"users_db": {}, "teachers_db": {}}
    return {"users_db": {}, "teachers_db": {}}

def save_database(db_data):
    """Мәліметтерді файлға жазып сақтау"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)

# Жедел жад пен файлдық базаны синхрондау
db = load_database()
if "users_db" not in str_web.session_state:
    str_web.session_state.users_db = db.get("users_db", {})
if "teachers_db" not in str_web.session_state:
    str_web.session_state.teachers_db = db.get("teachers_db", {})

# Пайдаланушылар сессиялары
if "current_user" not in str_web.session_state:
    str_web.session_state.current_user = None
if "current_teacher" not in str_web.session_state:
    str_web.session_state.current_teacher = None

# Оқушының қадамдық навигациясын бақылау
if "step" not in str_web.session_state:
    str_web.session_state.step = 2

# 🔐 МЕКТЕП ӘКІМШІЛІГІНІҢ ҚҰПИЯ СӨЗІ
SECRET_SCHOOL_CODE = "school_admin_2026"

# 📚 ЕКІ НЕГІЗГІ БЕЙІНДІК ПӘН БАЗАСЫ
COMBINATION_INFO = {
    "Физика - Математика": {
        "бағыт": "Жаратылыстану-математикалық бағыт (ЖМБ)",
        "грант_саны": "🔥 Шамамен 23,000+ грант (Мемлекеттік тапсырыс бойынша ең ірі үлес)",
        "статистика": "📊 ҰБТ қорытындысы бойынша техникалық және IT бағыттарға сұраныс өте жоғары. 99% грант игерілген.",
        "мамандықтар": [
            "📐 B009 Математика мұғалімдерін даярлау — Шекті балл: 75 | Орташа табыс: ~250,000 - 450,000 ₸",
            "🔬 B010 Физика мұғалімдерін даярлау — Шекті балл: 75 | Орташа табыс: ~250,000 - 450,000 ₸",
            "🌌 B054 Физика — Шекті балл: 50 | Орташа табыс: ~220,000 - 400,000 ₸",
            "📊 B055 Математика және статистика — Шекті балл: 50 | Орташа табыс: ~350,000 - 700,000 ₸",
            "⚙️ B056 Механика — Шекті балл: 50 | Орташа табыс: ~300,000 - 550,000 ₸",
            "📡 B059 Коммуникациялар және коммуникациялық технологиялар — Шекті балл: 50 | Орташа табыс: ~400,000 - 850,000 ₸",
            "🧪 B061 Материалтану және технологиялар — Шекті балл: 50 | Орташа табыс: ~280,000 - 500,000 ₸",
            "⚡ B062 Электр техникасы және электроэнергетика — Шекті балл: 50 | Орташа табыс: ~320,000 - 600,000 ₸",
            "🤖 B063 Электр техникасы және автоматтандыру — Шекті балл: 50 | Орташа табыс: ~350,000 - 750,000 ₸",
            "🔩 B064 Механика және металл өңдеу — Шекті балл: 50 | Орташа табыс: ~300,000 - 550,000 ₸",
            "🚗 B065 Көлік техникасы мен технологиялары — Шекті балл: 50 | Орташа табыс: ~280,000 - 600,000 ₸",
            "🚢 B066 Теңіз көлігі және технологиялары — Шекті балл: 50 | Орташа табыс: ~450,000 - 900,000 ₸",
            "✈️ B067 Әуе көлігі және технологиялары — Шекті балл: 50 | Орташа табыс: ~500,000 - 1,200,000 ₸",
            "⛏️ B071 Тау-кен ісі және пайдалы қазбаларды өндіру — Шекті балл: 50 | Орташа табыс: ~450,000 - 1,000,000 ₸",
            "🏗️ B074 Қала құрылысы, құрылыс жұмыстары — Шекті балл: 50 | Орташа табыс: ~350,000 - 750,000 ₸"
        ]
    },
    "Биология - Химия": {
        "бағыт": "Жаратылыстану-математикалық бағыт (ЖМБ)",
        "грант_саны": "📊 Шамамен 4,500+ грант (Бәсекелестік деңгейі жоғары бағыттардың бірі)",
        "статистика": "🩺 Денсаулық сақтау және медицина бағдарламалары бойынша іріктеу қатаң, шекті балл жоғары.",
        "мамандықтар": [
            "🧪 B012 Химия мұғалімдерін даярлау — Шекті балл: 75 | Орташа табыс: ~250,000 - 450,000 ₸",
            "🌿 B013 Биология мұғалімдерін даярлау — Шекті балл: 75 | Орташа табыс: ~250,000 - 450,000 ₸",
            "🧬 B050 Биологиялық және сабақтас ғылымдар — Шекті балл: 50 | Орташа табыс: ~240,000 - 500,000 ₸",
            "⚗️ B053 Химия — Шекті балл: 50 | Орташа табыс: ~230,000 - 480,000 ₸",
            "💊 B072 Фармацевтикалық өндіріс технологиясы — Шекті балл: 50 | Орташа табыс: ~300,000 - 650,000 ₸",
            "🐈 B083 Ветеринария — Шекті балл: 50 | Орташа табыс: ~250,000 - 500,000 ₸",
            "🩺 B084 Мейіргер ісі — Шекті балл: 70 | Орташа табыс: ~180,000 - 300,000 ₸",
            "💊 B085 Фармация — Шекті балл: 70 | Орташа табыс: ~280,000 - 550,000 ₸",
            "🏥 B086 Жалпы медицина — Шекті балл: 70 | Орташа табыс: ~350,000 - 800,000 ₸",
            "🦷 B087 Стоматология — Шекті балл: 70 | Орташа табыс: ~400,000 - 1,500,000 ₸",
            "👶 B088 Педиатрия — Шекті балл: 70 | Орташа табыс: ~300,000 - 650,000 ₸"
        ]
    }
}

# ==================== БҮЙІРЛІК ПАНЕЛЬ ====================
possible_paths = ["src/logo.jpg", "logo.jpg", "src/image_94be39.jpg", "image_94be39.jpg"]
logo_path = None
for path in possible_paths:
    if os.path.exists(path):
        logo_path = path
        break

if logo_path:
    str_web.sidebar.image(logo_path, use_container_width=True)
else:
    str_web.sidebar.markdown("<h2 style='text-align: center; color: #2b4c7e;'>🏫 №4 ГИМНАЗИЯ</h2>", unsafe_allow_html=True)

str_web.sidebar.markdown("### 🚪 Жүйе порты")
user_role = str_web.sidebar.radio("Режимді таңдаңыз:", ["🎒 Оқушы бұрышы", "👩‍🏫 Мұғалімдер кеңсесі"])

str_web.sidebar.markdown("---")
str_web.sidebar.markdown("**📊 Қазіргі статистика (Файлдан):**")
str_web.sidebar.write(f"Тіркелген оқушылар: **{len(str_web.session_state.users_db)}**")
str_web.sidebar.write(f"Тіркелген мұғалімдер: **{len(str_web.session_state.teachers_db)}**")


# ==================== 1-РЕЖИМ: ОҚУШЫЛАР БӨЛІМІ ====================
if user_role == "🎒 Оқушы бұрышы":
    str_web.title("🎓 Кәсіби бағдар беру жүйесі")  
    
    # 1-ҚАДАМ: ТІРКЕЛУ ЖӘНЕ КІРУ БЕТІ
    if str_web.session_state.current_user is None:
        str_web.subheader("🔐 1-Қадам: Кіру немесе Жүйеге тіркелу")
        c_auth1, c_auth2 = str_web.columns(2)
        
        with c_auth1:
            str_web.markdown("#### 🚪 Бұрын тіркелген болсаңыз, кіру")
            login_iin = str_web.text_input("ЖСН (ИИН) енгізіңіз:", max_chars=12, key="stud_login_iin_key")
            login_pass = str_web.text_input("Құпия сөз:", type="password", key="stud_login_pass_key")
            if str_web.button("Жүйеге кіру 🔓", key="stud_login_btn_key"):
                if login_iin in str_web.session_state.users_db and str_web.session_state.users_db[login_iin]["password"] == login_pass:
                    str_web.session_state.current_user = login_iin
                    if str_web.session_state.users_db[login_iin].get("survey_done", False):
                        str_web.session_state.step = 5
                    else:
                        str_web.session_state.step = 2
                    str_web.rerun()
                else:
                    str_web.error("ЖСН немесе құпия сөз қате!")

        current_iin = str_web.session_state.current_user
        user_folder = str_web.session_state.users_db[current_iin]
        
        # Егер мұғалім сыныпқа бөлген болса -> Нәтиже беті
        if "assigned_class" in user_folder:
            str_web.success("🎉 Құттықтаймыз! Сіздің нәтижеңіз дайын.")
            str_web.balloons()
            str_web.markdown(f"### 🎓 Сіз бөлінген сынып: **{user_folder['assigned_class']}**")
            str_web.info("Жаңа оқу жылында сәттілік тілейміз!")
            
            if str_web.button("Жүйеден шығу 🚪"):
                str_web.session_state.current_user = None
                str_web.session_state.step = 2
                str_web.rerun()
        
        # Әйтпесе, бұрынғыдай сауалнаманы толтыру қадамдары
        else:
            str_web.sidebar.info(f"👤 Кірген оқушы ЖСН: {current_iin}")
                else:
                        str_web.session_state.step = 2
                    str_web.rerun()
                else:
                    str_web.error("ЖСН немесе құпия сөз қате!")
                    
        with c_auth2:
            str_web.markdown("#### 📝 Алғашқы рет тіркелу")
            reg_iin = str_web.text_input("ЖСН (12 сан):", max_chars=12, key="stud_reg_iin_key")
            reg_pass = str_web.text_input("Құпия сөз ойлап табыңыз:", type="password", key="stud_reg_pass_key")
            if str_web.button("Тіркелу және Бастау 🚀", key="stud_reg_btn_key"):
                if len(reg_iin) != 12 or not reg_iin.isdigit():
                    str_web.error("ЖСН 12 саннан тұруы керек!")
                elif reg_iin in str_web.session_state.users_db:
                    str_web.warning("Бұл ЖСН тіркеліп қойған. Сол жақтан кіріңіз.")
                elif not reg_pass:
                    str_web.error("Құпия сөз өрісі бос!")
                else:
                    # Жаңа оқушыны жадқа және файлға тіркеу
                    str_web.session_state.users_db[reg_iin] = {
                        "password": reg_pass, 
                        "profile_done": False, 
                        "stats_read": False,      
                        "survey_done": False, 
                        "data": {}
                    }
                    save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
                    str_web.success("🎉 Тіркелу сәтті! Енді сол жақтағы терезеге ЖСН жазып жүйеге кіріңіз.")

    else:
        current_iin = str_web.session_state.current_user
        user_folder = str_web.session_state.users_db[current_iin]
        
        str_web.sidebar.info(f"👤 Кірген оқушы ЖСН: {current_iin}")
        if str_web.sidebar.button("Жүйеден шығу 🚪", key="logout_stud_side"):
            str_web.session_state.current_user = None
            str_web.session_state.step = 2
            str_web.rerun()
            
        # 2-ҚАДАМ: ЖЕКЕ МӘЛІМЕТТЕР МЕН БАҒАЛАР
        if str_web.session_state.step == 2:
            str_web.header("📋 2-Қадам: Жеке мәліметтер және пәндік үлгерімді толтыру")
            col_inputs, col_grades = str_web.columns(2)
            
            with col_inputs:
                str_web.markdown("**👤 Оқушы аты-жөні:**")
                saved_data = user_folder.get("data", {})
                st_lastname = str_web.text_input("Тегі (Фамилия):", value=saved_data.get("Тегі", ""), key="st_lastname_input")
                st_firstname = str_web.text_input("Аты:", value=saved_data.get("Аты", ""), key="st_firstname_input")
                st_gender = str_web.selectbox("Жынысы:", ["Ұл", "Қыз"], index=0 if saved_data.get("Жынысы") == "Ұл" else 1, key="st_gender_select")
                st_class = str_web.selectbox("Қазіргі сыныбыңыз:", ["9 'А'", "9 'Ә'", "9 'Б'", "9 'В'", "9 'Г'"], key="st_class_select")
            
            with col_grades:
                str_web.markdown("**📚 Ағымдағы 9-сынып бағаларыңыз (3, 4, 5):**")
                g_alg = str_web.radio("Алгебра:", [5, 4, 3], horizontal=True, key="g_alg_r")
                g_geo = str_web.radio("Геометрия:", [5, 4, 3], horizontal=True, key="g_geo_r")
                g_fiz = str_web.radio("Физика:", [5, 4, 3], horizontal=True, key="g_fiz_r")
                g_bio = str_web.radio("Биология:", [5, 4, 3], horizontal=True, key="g_bio_r")
                g_xim = str_web.radio("Химия:", [5, 4, 3], horizontal=True, key="g_xim_r")
                
            if str_web.button("Сақтау және Статистика бетіне өту ➡️", type="primary", key="save_profile_btn"):
                if not st_lastname or not st_firstname:
                    str_web.error("Тегі мен Аты өрістерін міндетті түрде толтырыңыз!")
                else:
                    total_points = g_alg + g_geo + g_fiz + g_bio + g_xim + 20 # басқа пәндерге шартты балл
                    calculated_gpa = total_points / 9
                    
                    user_folder["data"].update({
                        "ЖСН": current_iin, "Тегі": st_lastname.strip(), "Аты": st_firstname.strip(), 
                        "Жынысы": st_gender, "Сыныбы": st_class, "Ұпай Саны": total_points, "Орташа балл": calculated_gpa,
                        "Комбинация": "Физика - Математика", 
                        "Алгебра": g_alg, "Геометрия": g_geo, "Физика": g_fiz, "Биология": g_bio, "Химия": g_xim
                    })
                    user_folder["profile_done"] = True
                    save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
                    str_web.session_state.step = 3
                    str_web.rerun()

        # 3-ҚАДАМ: МЕМЛЕКЕТТІК ГРАНТТАР СТАТИСТИКАСЫ БЕТІ
        elif str_web.session_state.step == 3:
            str_web.header("🏛️ 3-Қадам: Ресми мемлекеттік білім беру гранттарының есебі (gov.kz)")
            str_web.markdown("##### 2025-2026 оқу жылына 77 мыңнан астам білім беру гранты бөлінді")
            
            c_gr1, c_gr2, c_gr3 = str_web.columns(3)
            with c_gr1:
                str_web.metric(label="Бакалавриатқа бөлінген жалпы грант", value="77 000+", delta="99% Игерілді")
            with c_gr2:
                str_web.metric(label="Конкурсқа түскен жалпы өтініш", value="112 873", delta="Жоғары бәсеке")
            with c_gr3:
                str_web.metric(label="«Серпін» бағдарламасы гранттары", value="2 412", delta="83% Игерілді")
                
            str_web.markdown("""
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 5px solid #3182ce; margin-top: 15px;">
                <h4 style="color: #2b6cb0; margin-top:0;">🔰 2025-2026 оқу жылына арналған ресми мәліметтер:</h4>
                <ul style="font-size: 15px; line-height: 1.8;">
                    <li>🏛️ Мемлекеттік білім беру тапсырысы аясында бакалавриат деңгейіне <b>77 мыңнан астам грант</b> бөлінді.</li>
                    <li>⚡ Конкурс нәтижесінде мемлекеттік білім беру тапсырысының <b>99%-ы игерілді</b>.</li>
                    <li>💡 Қазақстанда ашылып жатқан <b>шетелдік жоғары оқу орындарының филиалдарына 2 365 грант</b> бөлінді.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            c_nav1, c_nav2 = str_web.columns(2)
            with c_nav1:
                if str_web.button("⬅️ Артқа (Профильге оралу)", key="back_to_2"):
                    str_web.session_state.step = 2
                    str_web.rerun()
            with c_nav2:
                if str_web.button("Мәліметтермен таныстым. Сауалнамаға өту ➡️", type="primary", key="read_stats_btn"):
                    user_folder["stats_read"] = True
                    save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
                    str_web.session_state.step = 4
                    str_web.rerun()

        # 4-ҚАДАМ: ЖАҒДАЯТТЫҚ САУАЛНАМА БЕТІ
        elif str_web.session_state.step == 4:
            str_web.header("📝 4-Қадам: Жағдаяттық психологиялық сауалнама")
            
            with str_web.form("situational_survey_form"):
                q1 = str_web.radio("1. Жағдаят: Мұғалім шұғыл жоба тапсырды. Сіз не істейсіз?", ["A) Бастаманы қолға алып, жауапкершілікті бөлемін.", "B) Нақты міндет жүктелгенін күтемін, өз бөлімімді мінсіз істеймін."], key="q1_k")
                q2 = str_web.radio("2. Жағдаят: Топтық жұмыста сыныптастарыңыз дауласса не істейсіз?", ["A) Ортаға түсіп, компромисс ұсынамын.", "B) Дауға араласпай, өз жұмысымды жалғастырамын."], key="q2_k")
                q3 = str_web.radio("3. Жағдаят: Көпшілік алдында сөз сөйлеу мүмкіндігі берілсе?", ["A) Маған мотивация береді (Экстраверт).", "B) Артта отырып зерттеу жасағанды қалаймын (Интроверт)."], key="q3_k")
                
                submit_survey = str_web.form_submit_button("Сауалнаманы аяқтау және Қорытынды бетке өту 🏁")
                
                if submit_survey:
                    leader_score = sum([1 for ans in [q1, q2, q3] if ans.startswith("A)")])
                    is_leader = 1 if leader_score >= 2 else 0
                    vibe_type = "Белсенді" if "A)" in q3 else "Тұрақты"
                    
                    user_folder["data"].update({
                        "Лидер Анықтамасы": is_leader, 
                        "Лидер Ұпайы": leader_score,
                        "Вайб": vibe_type
                    })
                    user_folder["survey_done"] = True
                    save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
                    str_web.session_state.step = 5
                    str_web.rerun()
            
            if str_web.button("⬅️ Кері қайту (Статистика бетіне)", key="back_to_3"):
                str_web.session_state.step = 3
                str_web.rerun()
                    
        # 5-ҚАДАМ: ТАҢДАУ ЖӘНЕ КӘСІБИ ТАЛДАУ БЕТІ
        elif str_web.session_state.step == 5:
            str_web.success(f"🎉 Құрметті {user_folder['data'].get('Аты', '')}, барлық қадамдар аяқталды! Деректеріңіз файлға сәтті сақталды.")
            
            str_web.header("🎯 5-Қадам: Бейінді пәндер комбинациясын таңдау және Кәсіби есеп")
            
            # Оқушы осы жерден өз комбинациясын таңдайды
            chosen_combo = str_web.selectbox(
                "👇 Төмендегі тізімнен өзіңізге қажетті Бейінді пәндер комбинациясын таңдаңыз:", 
                list(COMBINATION_INFO.keys()), 
                key="final_page_combo_select"
            )
            
            # Тікелей файлға және жадқа жазу (ауыстырған сайын сақталады)
            user_folder["data"]["Комбинация"] = chosen_combo
            user_folder["data"]["Бағыты"] = COMBINATION_INFO[chosen_combo]["бағыт"]
            save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
            
            info = COMBINATION_INFO[chosen_combo]
            
            str_web.markdown(f"""
            <div style="background-color: #f0f4f8; padding: 25px; border-radius: 8px; border-left: 6px solid #2b4c7e; margin-top: 15px;">
                <h3 style="color: #2b4c7e; margin-top: 0; font-size:22px;">🏛️ Таңдалған бағыт: {info['бағыт']} ({chosen_combo})</h3>
                <p style="font-size: 16px; margin: 8px 0;"><b>🎁 Мемлекеттік грант мүмкіндіктері:</b> {info['грант_саны']}</p>
                <p style="font-size: 16px; margin: 8px 0; color: #2b6cb0;"><b>📈 Нарыққа талдау сипаттамасы:</b> {info['статистика']}</p>
                <hr style="border: 0; border-top: 1px solid #cbd5e0; margin: 20px 0;">
                <h4 style="color: #2c5282; margin-bottom: 15px;">💼 Осы комбинация бойынша мамандықтар, шекті баллдар және орташа табыс:</h4>
                <ul style="padding-left: 25px; font-size: 15px; line-height: 2;">
                    {"".join([f"<li style='margin-bottom:8px; list-style-type: square;'>{job}</li>" for job in info['мамандықтар']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            str_web.write("---")
            c_fin1, c_fin2 = str_web.columns(2)
            with c_fin1:
                if str_web.button("⬅️ Сауалнаманы қайта тапсыру (Артқа қайту)", key="back_to_4"):
                    str_web.session_state.step = 4
                    str_web.rerun()
            with c_fin2:
                if str_web.button("🏁 Аяқтау және Жүйеден шығу", type="primary", key="complete_and_logout"):
                    str_web.session_state.current_user = None
                    str_web.session_state.step = 2
                    str_web.success("Мәліметтеріңіз толық бекітілді! Сау болғыңыз!")
                    str_web.rerun()


# ==================== 2-РЕЖИМ: МҰҒАЛІМДЕР БӨЛІМІ ====================
elif user_role == "👩‍🏫 Мұғалімдер кеңсесі":
    str_web.title("🛠 Мектеп әкімшілігі мен мұғалімдерге арналған жабық панель")  
    
    if str_web.session_state.current_teacher is None:
        str_web.subheader("🔒 Жауапты мұғалімдерді верификациялау")
        t_auth1, t_auth2 = str_web.columns(2)
        
        with t_auth1:
            str_web.markdown("#### 🚪 Жүйеге кіру")
            t_log_iin = str_web.text_input("Мұғалім ЖСН:", max_chars=12, key="teach_login_iin_key")
            t_log_pass = str_web.text_input("Құпия сөз:", type="password", key="teach_login_pass_key")
            if str_web.button("Кіру 🔓", key="teach_login_btn_key"):
                if t_log_iin in str_web.session_state.teachers_db and str_web.session_state.teachers_db[t_log_iin]["password"] == t_log_pass:
                    str_web.session_state.current_teacher = t_log_iin
                    str_web.rerun()
                else:
                    str_web.error("Қате маліметтер!")
                    
        with t_auth2:
            str_web.markdown("#### 📝 Жаңа Мұғалімді базаға тіркеу")
            t_reg_name = str_web.text_input("Мұғалімнің аты-жөні (ФИО):", key="teach_reg_name_key")
            t_reg_iin = str_web.text_input("ЖСН (12 сан):", max_chars=12, key="teach_reg_iin_key")
            t_reg_pass = str_web.text_input("Құпия сөз:", type="password", key="teach_reg_pass_key")
            t_school_code = str_web.text_input("🔑 Мектеп коды:", type="password", key="teach_school_code_key")
            
            if str_web.button("Мұғалімді тіркеу 🚀", key="teach_reg_btn_key"):
                if t_school_code.strip() == SECRET_SCHOOL_CODE:
                    str_web.session_state.teachers_db[t_reg_iin] = {"name": t_reg_name.strip(), "password": t_reg_pass}
                    save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
                    str_web.success("Мұғалім тіркелді!")
                    str_web.rerun()

    else:
        current_t_iin = str_web.session_state.current_teacher
        teacher_name = str_web.session_state.teachers_db[current_t_iin]["name"]
        str_web.sidebar.success(f"👩‍🏫 {teacher_name}")
        
        if str_web.sidebar.button("Жүйеден шығу 🚪", key="logout_teach"):
            str_web.session_state.current_teacher = None
            str_web.rerun()

        # === ОҚУШЫНЫ СЫНЫПҚА БӨЛУ ЖӘНЕ ӨШІРУ ===
        str_web.markdown("---")
        str_web.subheader("🛠 Оқушыларды басқару панелі")
        all_iins = list(str_web.session_state.users_db.keys())
        target_iin = str_web.selectbox("Оқушыны таңдаңыз:", all_iins)
        
        col_m1, col_m2 = str_web.columns(2)
        with col_m1:
            class_choice = str_web.selectbox("Сыныпқа бөлу:", ["10 'А'", "10 'Ә'", "10 'Б'"])
            if str_web.button("💾 Сыныпқа бекіту"):
                str_web.session_state.users_db[target_iin]["assigned_class"] = class_choice
                save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
                str_web.success(f"Оқушы {class_choice} сыныбына бекітілді!")
                str_web.rerun()
        
        with col_m2:
            if str_web.button("❌ Оқушыны базадан өшіру", type="primary"):
                del str_web.session_state.users_db[target_iin]
                save_database({"users_db": str_web.session_state.users_db, "teachers_db": str_web.session_state.teachers_db})
                str_web.success("Оқушы жойылды!")
                str_web.rerun()
        # ==========================================

        completed_students = [u["data"] for u in str_web.session_state.users_db.values() if u.get("profile_done") and u.get("survey_done")]
        
        if not completed_students:
            str_web.info("Сауалнамадан өткен оқушылар әлі жоқ.")
        else:
            df = pd.DataFrame(completed_students)
            str_web.markdown("### 📋 Түлектердің толық академиялық ведомосы")
            str_web.dataframe(df)
            
            str_web.write("---")
            str_web.subheader("⚡ Интеллектуалды Зигзаг алгоритмі арқылы сыныптарға бөлу")
            list_view = ["Тегі","Аты","Сыныбы","Орташа балл","Комбинация"]

            if str_web.button("💫 Сыныптарды жинақтауды бастау", key="zigzag_start_btn"):
                # ... (бұрынғы алгоритм кодыңызды осы жерге қоясыз)
                str_web.write("Алгоритм жұмыс істеді.")
                
                # 1. ФИЗИКА-МАТЕМАТИКА БӨЛІМІ
                fm_pool = df[df["Комбинация"] == "Физика - Математика"].copy()
                str_web.markdown("### 🎯 ФИЗИКА - МАТЕМАТИКА БАҒЫТЫ")
                if not fm_pool.empty:
                    fm_pool = fm_pool.sort_values(by="Орташа балл", ascending=False).reset_index(drop=True)
                    fm_a, fm_ae = [], []
                    for idx, row in fm_pool.iterrows():
                        if idx % 2 == 0: fm_a.append(row)
                        else: fm_ae.append(row)
                    
                    c1, c2 = str_web.columns(2)
                    with c1:
                        str_web.info("🏫 10 'А' сыныбы (Физ-Мат)")
                        str_web.dataframe(pd.DataFrame(fm_a)[list_view])
                    with c2:
                        str_web.success("🏫 10 'Ә' сыныбы (Физ-Мат)")
                        str_web.dataframe(pd.DataFrame(fm_ae)[list_view])
                
                # 2. БИОЛОГИЯ-ХИМИЯ БӨЛІМІ
                bx_pool = df[df["Комбинация"] == "Биология - Химия"].copy()
                str_web.markdown("### 🎯 БИОЛОГИЯ - ХИМИЯ БАҒЫТЫ")
                if not bx_pool.empty:
                    str_web.error("🏫 10 'Б' сыныбы (Био-Хим)")
                    str_web.dataframe(bx_pool[list_view])
