"""
MySQL 資料庫連接模組
提供與 MySQL 資料庫的連接和操作功能
"""

import os
import mysql.connector  # 導入 MySQL 連接器，用於與 MySQL 資料庫進行互動


def get_db_connection():
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME', 'appointment_system')

    if not db_password:
        raise ValueError("缺少 DB_PASSWORD 環境變數，請先設定資料庫密碼")

    # 建立與 MySQL 資料庫的連接
    connection = mysql.connector.connect(
        # 資料庫主機位置
        host=db_host,
        # 資料庫使用者名稱
        user=db_user,
        # 資料庫密碼
        password=db_password,
        # 要連接的資料庫名稱
        database=db_name
    )
    # 返回資料庫連接物件
    return connection


class Account:
    """
    帳號類別：用於管理使用者帳號資訊
    """

    def __init__(self, accountID, account, password, role):
        """
        初始化帳號物件
        參數說明：
        accountID: 帳號唯一識別碼
        account: 使用者帳號名稱（通常是電子郵件）
        password: 帳號密碼
        role: 使用者角色 (0:學生, 1:教授, 2:秘書)
        """
        self.accountID = accountID    # 帳號ID
        self.account = account        # 帳號名稱
        self.password = password      # 帳號密碼
        self.role = role             # 使用者角色


def get_account_by_account(account):
    """
    根據帳號名稱查詢使用者帳號資訊
    參數：
    account: 使用者帳號名稱（通常是電子郵件）
    返回：
    如果找到帳號，返回 Account 物件
    如果未找到，返回 None
    """
    # 建立資料庫連接
    connection = get_db_connection()
    # 建立游標物件，設定返回字典格式的結果
    cursor = connection.cursor(dictionary=True)
    # 不安全的寫法（容易遭受 SQL Injection）：
    # query = f"SELECT * FROM account WHERE account = '{account}'"
    # 安全的寫法（使用參數化查詢）：
    # SQL 查詢語句，使用參數化查詢防止 SQL Injection
    query = "SELECT * FROM account WHERE account = %s"
    # %s 會被 cursor.execute() 中的參數自動替換
    # 參數會被正確地轉義（escape）和格式化
    # 例子：
    # account = "test@email.com"
    # cursor.execute("SELECT * FROM account WHERE account = %s", (account,))
    # 實際執行的 SQL 會像：SELECT * FROM account WHERE account = 'test@email.com'
    # 執行查詢，傳入帳號參數
    cursor.execute(query, (account,))   # 傳入一個單元素的元組 (tuple)
    # 支援多個參數
    # 多個參數的例子：
    # cursor.execute("SELECT * FROM account WHERE account = %s AND password = %s",
    #               (account, password))
    # 獲取查詢結果的第一行
    row = cursor.fetchone()
    # 關閉游標
    cursor.close()
    # 關閉資料庫連接
    connection.close()
    # 印出查詢的帳號（用於除錯）
    print(f"user_account: {account}")
    # 如果找到帳號資料
    if row:
        # 將查詢結果轉換為 Account 物件並返回
        return Account(**row)
    # 如果未找到帳號資料，返回 None
    return None


def get_professors():
    """
    獲取所有教授的基本資訊
    返回：
    包含所有教授資料的列表，每個教授包含：
    - name: 教授姓名
    - professorship: 教授職稱
    - photo: 教授照片
    - professorID: 教授ID
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, professorship, photo, professorID FROM professor")
    # 獲取所有查詢結果
    professors = cursor.fetchall()
    connection.close()
    # 返回教授資料列表
    return professors


def get_account_by_account_id(account_id):
    """
    根據帳號ID查詢使用者帳號資訊
    參數：
    account_id: 帳號唯一識別碼
    返回：
    如果找到帳號，返回帳號資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM account where accountID = %s", (account_id,))
    account = cursor.fetchone()
    connection.close()
    return account


def get_professor_by_id(professor_id):
    """
    根據教授ID查詢教授資訊
    參數：
    professor_id: 教授唯一識別碼
    返回：
    如果找到教授，返回教授資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM professor WHERE professorID = %s", (professor_id,))
    professor = cursor.fetchone()
    connection.close()
    return professor


def get_otherinfo(professor_id):
    """
    獲取教授的其他相關資訊（如實驗室資訊、研究領域等）
    參數：
    professor_id: 教授唯一識別碼
    返回：
    如果找到資訊，返回包含其他資訊的元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM otherinfo WHERE professorID = %s", (professor_id,))
    otherinfo = cursor.fetchone()
    connection.close()
    return otherinfo


def get_appointmentslot(professor_id):
    """
    獲取教授的預約時段資訊
    參數：
    professor_id: 教授唯一識別碼
    返回：
    如果找到資訊，返回包含預約時段的元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM appointmentslot WHERE professorID = %s", (professor_id,))
    appointmentslot = cursor.fetchone()
    connection.close()
    return appointmentslot


def get_professor_by_account_id(account_id):
    """
    根據帳號ID查詢對應的教授資訊
    參數：
    account_id: 帳號唯一識別碼
    返回：
    如果找到教授，返回教授資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM professor WHERE accountID = %s", (account_id,))
    professor = cursor.fetchone()
    connection.close()
    return professor


def update_appointment_slots(professor_id, new_slot):
    """
    更新教授的預約時段資訊
    參數：
    professor_id: 教授唯一識別碼
    new_slot: 新的預約時段資訊
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE appointmentslot SET availableTimeInfo = %s WHERE professorID = %s", (new_slot, professor_id))
    # 提交資料庫變更
    connection.commit()
    connection.close()


def update_notice(professor_id, new_notice):
    """
    更新教授的面試注意事項
    參數：
    professor_id: 教授唯一識別碼
    new_notice: 新的面試注意事項內容
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE otherinfo SET interviewPrecautions = %s WHERE professorID = %s", (new_notice, professor_id))
    connection.commit()
    connection.close()


def update_lab_rule(professor_id, new_lab_rule):
    """
    更新教授的實驗室規則/說明
    參數：
    professor_id: 教授唯一識別碼
    new_lab_rule: 新的實驗室規則/說明內容
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE otherinfo SET labDescription = %s WHERE professorID = %s",
                   (new_lab_rule, professor_id))
    connection.commit()
    connection.close()


def update_research_area(professor_id, new_research_area):
    """
    更新教授的研究領域資訊
    參數：
    professor_id: 教授唯一識別碼
    new_research_area: 新的研究領域內容
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE otherinfo SET researchField = %s WHERE professorID = %s",
                   (new_research_area, professor_id))
    connection.commit()
    connection.close()


def update_reservationOpen_status(professor_id, new_status):
    """
    更新教授的預約開放狀態
    參數：
    professor_id: 教授唯一識別碼
    new_status: 新的預約開放狀態 (0:關閉預約, 1:開放預約）
    """
    # 印出更新資訊（用於除錯）
    print(f"professor_id: {professor_id}, new_status: {new_status}")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE otherinfo SET reservationOpen = %s WHERE professorID = %s", (new_status, professor_id))
    connection.commit()
    connection.close()


def get_student_count(professor_id):
    """
    獲取特定教授目前指導的學生人數
    參數：
    professor_id: 教授唯一識別碼
    返回：
    已接受指導的學生人數 (status = 1 表示已接受指導）
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM mentorshiprequest WHERE professorID = %s AND status = 1", (professor_id,))
    # 獲取查詢結果（計數值）
    student_count = cursor.fetchone()[0]
    connection.close()
    return student_count


def get_student_by_account_id(account_id):
    """
    根據帳號ID查詢對應的學生資訊
    參數：
    account_id: 帳號唯一識別碼
    返回：
    如果找到學生，返回學生資訊元組
    如果未找到，返回 None
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, email, phone, department, admissionYear, rankType, rank, studentID, photo FROM student WHERE accountID = %s", (account_id,))
    student = cursor.fetchone()
    connection.close()
    return student


def update_student_profile(account_id, name, password, account, email, phone, photo):
    """
    更新學生的個人資料
    參數：
    account_id: 帳號唯一識別碼
    name: 學生姓名
    password: 帳號密碼
    account: 帳號名稱（通常是電子郵件）
    email: 電子郵件
    phone: 電話號碼
    photo: 照片檔案（可選）
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    # 根據是否有上傳照片執行不同的更新語句
    if photo:
        # 如果有照片，更新學生資料（包含照片）
        cursor.execute("UPDATE student SET name = %s, email = %s, phone = %s, photo = %s WHERE accountID = %s",
                       (name, email, phone, photo, account_id))
    else:
        # 如果沒有照片，更新學生資料（不包含照片）
        cursor.execute("UPDATE student SET name = %s, email = %s, phone = %s WHERE accountID = %s",
                       (name, email, phone, account_id))
    cursor.execute("UPDATE account SET account = %s, password = %s WHERE accountID = %s",
                   (account, password, account_id))
    connection.commit()
    connection.close()


def update_professor_profile(account_id, name, password, account, professorship, email, phone, photo):
    """
    更新教授的個人資料
    參數：
    account_id: 帳號唯一識別碼
    name: 教授姓名
    password: 帳號密碼
    account: 帳號名稱（通常是電子郵件）
    professorship: 教授職稱
    email: 電子郵件
    phone: 電話號碼
    photo: 照片檔案（可選）
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    if photo:
        # 如果有照片，更新教授資料（包含照片）
        cursor.execute("UPDATE professor SET name = %s, professorship = %s, email = %s, phone = %s, photo = %s WHERE accountID = %s",
                       (name, professorship, email, phone, photo, account_id))
    else:
        # 如果沒有照片，更新教授資料（不包含照片）
        cursor.execute("UPDATE professor SET name = %s, professorship = %s, email = %s, phone = %s WHERE accountID = %s",
                       (name, professorship, email, phone, account_id))
    cursor.execute("UPDATE account SET account = %s, password = %s WHERE accountID = %s",
                   (account, password, account_id))
    connection.commit()
    connection.close()


def create_appointment(professor_id, student_id, start_time, end_time, resume_filename, note=''):
    """
    創建預約面談記錄
    參數說明：
    professor_id: 教授ID
    student_id: 學生帳號ID
    start_time: 預約開始時間
    end_time: 預約結束時間
    resume_filename: 履歷檔案名稱
    note: 備註(可選)
    返回：
    成功時返回 True ; 失敗時拋出異常
    """
    connection = get_db_connection()
    # 建立具有緩衝功能的游標，避免未讀取結果就執行新查詢的問題
    cursor = connection.cursor(buffered=True)
    try:
        # 檢查學生是否已存在於資料庫
        cursor.execute("""
            SELECT studentID, name FROM student WHERE accountID = %s
        """, (student_id,))
        student_result = cursor.fetchone()

        if student_result:
            # 如果學生存在，直接使用現有的學生ID
            actual_student_id = student_result[0]
        else:
            # 如果學生不存在，則從 account 表獲取基本資訊
            cursor.execute(
                "SELECT account FROM account WHERE accountID = %s", (student_id,))
            account_info = cursor.fetchone()
            # 使用電子郵件作為基本資訊
            student_email = account_info[0]
            # 從電子郵件中提取用戶名作為學生姓名
            student_name = student_email.split('@')[0]

            # 插入新學生資料，設定預設的考試資訊
            cursor.execute("""
                INSERT INTO student 
                (accountID, name, email, phone, department, admissionYear, rankType, `rank`)
                VALUES 
                (%s, %s, %s, '09REDACTED_PASSWORD', '資管系', '113', '考試-備取', 1)
            """, (student_id, student_name, student_email))
            # 提交新學生資料
            connection.commit()
            # 獲取新插入記錄的 ID
            actual_student_id = cursor.lastrowid

        # 創建預約記錄（status = 0 表示待回覆狀態）
        cursor.execute("""
            INSERT INTO appointment 
            (professorID, studentID, startTime, endTime, resume, note, status, requestDate, approvalDate)
            VALUES 
            (%s, %s, %s, %s, %s, %s, 0, CURDATE(), NULL)
        """, (professor_id, actual_student_id, start_time, end_time, resume_filename, note))
        # 提交預約記錄
        connection.commit()
        return True

    except Exception as e:
        # 發生錯誤時印出錯誤訊息並回滾交易
        print(f"預約創建錯誤: {str(e)}")
        connection.rollback()
        raise   # 重新拋出異常

    finally:
        # 確保資源被正確釋放
        cursor.close()
        connection.close()


def get_appointments_by_professor(professor_id):
    """
    獲取特定教授的所有預約記錄
    參數：
    professor_id: 教授唯一識別碼
    返回：
    包含所有預約記錄的列表，每筆記錄包含：
    - 預約相關資訊 (a.*)
    - 學生姓名
    - 考試類型和名次
    - 完整排名資訊
    - 學生信箱
    排序方式：
    1. 優先按申請日期降序（新的在前）
    2. 其次按考試名次升序（排名好的在前）
    """
    connection = get_db_connection()
    # 建立游標，設定返回字典格式的結果
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                a.*,                     -- 所有預約表的欄位
                s.name as student_name,  -- 學生姓名（重新命名避免欄位名稱衝突）
                s.rankType,              -- 考試類型（如：考試分發、申請入學）
                s.rank,                  -- 名次（數字）
                CASE 
                    WHEN s.rankType IS NOT NULL AND s.rank IS NOT NULL 
                    THEN CONCAT(
                        s.rankType,      -- 組合考試類型
                        CAST(s.rank as CHAR)  -- 將名次轉為字串並連接
                    )
                    ELSE '尚未設定'      -- 若資料不完整則顯示預設值
                END as rank_info,        -- 完整排名資訊 (例: 考試分發1)
                s.email                  -- 學生信箱
            FROM appointment a
            JOIN student s ON a.studentID = s.studentID  -- 關聯預約表和學生表
            WHERE a.professorID = %s     -- 篩選特定教授的預約
            ORDER BY 
                a.requestDate DESC,      -- 優先按申請日期降序排列
                s.rank ASC               -- 次要按名次升序排列
        """
        cursor.execute(query, (professor_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_appointments_by_student(account_id):
    """
    獲取特定學生的所有預約記錄
    參數：
    account_id: 學生帳號ID
    返回：
    包含所有預約記錄的列表，每筆記錄包含：
    - 預約相關資訊（時間、狀態等）
    - 教授姓名
    - 教授照片
    排序方式：
    - 按申請日期降序（新的在前）
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                a.*,                     -- 預約相關資訊
                p.name as professor_name, -- 教授姓名
                p.photo                  -- 教授照片
            FROM appointment a
            JOIN professor p ON a.professorID = p.professorID  -- 關聯預約表和教授表
            JOIN student s ON a.studentID = s.studentID        -- 關聯預約表和學生表
            WHERE s.accountID = %s       -- 篩選特定學生的預約
            ORDER BY a.requestDate DESC   -- 按申請日期做降序排序
        """
        cursor.execute(query, (account_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def update_appointment_status(appointment_id, new_status, approval_date=None):
    """
    更新預約狀態
    參數：
    appointment_id: 預約記錄的唯一識別碼
    new_status: 新的預約狀態
        0: 待回覆
        1: 已確認
        2: 已拒絕
    approval_date: 審核日期（可選）
        - 如果提供，會同時更新審核日期
        - 如果不提供，只更新狀態
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # 根據是否提供審核日期執行不同的更新語句
    if approval_date:
        # 更新狀態和審核日期
        query = """
            UPDATE appointment 
            SET status = %s, approvalDate = %s 
            WHERE appointmentID = %s
        """
        cursor.execute(query, (new_status, approval_date, appointment_id))
    else:
        # 只更新狀態
        query = "UPDATE appointment SET status = %s WHERE appointmentID = %s"
        cursor.execute(query, (new_status, appointment_id))
    connection.commit()
    cursor.close()
    connection.close()


def get_all_professors():
    """
    獲取所有教授的資料
    返回：
    包含所有教授資訊的列表，每筆記錄包含：
    - 教授基本資料 (p.*)
    - 帳號資訊 (account, password)
    - 其他相關資訊 (otherInfo表的所有欄位)
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT p.*, a.account, a.password, o.*
        FROM professor p
        JOIN account a ON p.accountID = a.accountID
        JOIN otherInfo o ON p.professorID = o.professorID;
    """)
    professors = cursor.fetchall()
    connection.close()
    return professors


def get_all_students():
    """
    獲取所有學生的資料
    返回：
    包含所有學生資訊的列表，每筆記錄包含：
    - 學生基本資料 (s.*)
        - studentID: 學生ID
        - accountID: 帳號ID
        - name: 姓名
        - email: 電子郵件
        - phone: 電話
        - department: 系所
        - admissionYear: 入學年度
        - rankType: 考試類型
        - rank: 名次
        - photo: 照片
    - 帳號資訊
        - account: 帳號名稱
        - password: 密碼
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT s.*, a.account, a.password
        FROM student s
        JOIN account a ON s.accountID = a.accountID
    """)
    students = cursor.fetchall()
    connection.close()
    return students


def delete_student(account_id):
    """
    刪除學生帳號及相關資料
    參數：
    account_id: 學生帳號的唯一識別碼

    處理流程：
    1. 刪除 student 表中的學生資料
    2. 刪除 account 表中的帳號資料
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 刪除學生資料
        cursor.execute(
            "DELETE FROM student WHERE accountID = %s", (account_id,))
        # 刪除帳號資料
        cursor.execute(
            "DELETE FROM account WHERE accountID = %s", (account_id,))

        connection.commit()

    except Exception as e:
        # 發生錯誤時回滾交易
        print(f"刪除學生資料時發生錯誤: {str(e)}")
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def delete_professor(account_id):
    """
    刪除教授帳號及相關資料
    參數：
    account_id: 教授帳號的唯一識別碼

    處理流程：
    1. 刪除 professor 表中的教授資料
    2. 刪除 account 表中的帳號資料
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 刪除教授資料
        cursor.execute(
            "DELETE FROM professor WHERE accountID = %s", (account_id,))
        # 刪除帳號資料
        cursor.execute(
            "DELETE FROM account WHERE accountID = %s", (account_id,))

        connection.commit()

    except Exception as e:
        # 發生錯誤時回滾交易
        print(f"刪除教授資料時發生錯誤: {str(e)}")
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def create_student_account(name, email, rankType, rank, department, admissionYear):
    """
    創建新的學生帳號
    參數：
    name: 學生姓名
    email: 電子郵件（同時作為帳號使用）
    rankType: 考試類型（如：考試分發、申請入學）
    rank: 名次
    department: 系所
    admissionYear: 入學年度

    處理流程：
    1. 在 account 表中創建帳號 (role=0 表示學生身份）
    2. 在 student 表中創建學生基本資料
    """
    # 除錯用：印出所有傳入的參數
    print(f"name: {name, email, rankType, rank, department, admissionYear}")
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 插入帳號資料（role=0 代表學生身份）
        cursor.execute(
            "INSERT INTO account (account, role) VALUES (%s, %s)", (email, 0,))
        account_id = cursor.lastrowid

        # 插入學生基本資料
        cursor.execute("""
            INSERT INTO student (accountID, name, rankType, rank, department, admissionYear, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (account_id, name, rankType, rank, department, admissionYear, email))

        connection.commit()

    except Exception as e:
        # 發生錯誤時回滾交易
        print(f"創建學生帳號時發生錯誤: {str(e)}")
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def create_pro_account(name, email, department, professorship, location, labStudentNum):
    """
    創建新的教授帳號
    參數：
    name: 教授姓名
    email: 電子郵件（同時作為帳號使用）
    department: 系所
    professorship: 職稱
    location: 研究室位置
    labStudentNum: 實驗室學生人數上限

    處理流程：
    1. 在 account 表中創建帳號 (role=1 表示教授身份）
    2. 在 professor 表中創建教授基本資料
    3. 在 otherInfo 表中創建教授其他資訊
    4. 在 appointmentslot 表中創建預約時段設定
    """
    # 除錯用：印出所有傳入的參數
    print(f"name: {name, email, department, professorship}")
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 插入帳號資料（role=1 代表教授身份）
        cursor.execute(
            "INSERT INTO account (account, role) VALUES (%s, %s)", (email, 1,))
        account_id = cursor.lastrowid

        # 插入教授基本資料
        cursor.execute("""
            INSERT INTO professor (accountID, name, email, department, professorship)
            VALUES (%s, %s, %s, %s, %s)
        """, (account_id, name, email, department, professorship,))
        professor_id = cursor.lastrowid
        print(f"professor_id: {professor_id}")  # 除錯用：印出教授ID

        # 插入教授其他資訊
        cursor.execute("""
            INSERT INTO otherInfo (professorID, location, labStudentNum)
            VALUES (%s, %s, %s)
        """, (professor_id, location, labStudentNum,))

        # 創建預約時段設定
        cursor.execute("""
            INSERT INTO appointmentslot (professorID)
            VALUES (%s)
        """, (professor_id,))

        connection.commit()

    except Exception as e:
        # 發生錯誤時回滾交易
        print(f"創建教授帳號時發生錯誤: {str(e)}")
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# 以下內容為秉謙在這個專案中所撰寫的程式碼
def get_all_professor_names():
    """
    獲取所有教授的姓名列表

    返回：
    list: 包含所有教授姓名的列表
    例如：['張教授', '李教授', '王教授']
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 從 professor 表中獲取所有教授的名字
        cursor.execute("SELECT name FROM professor ORDER BY name")  # 按姓名排序
        professors = cursor.fetchall()

        # 將查詢結果轉換為名字列表並返回
        # fetchall() 返回的是元組列表 [(name1,), (name2,)]
        # 使用列表推導式取出每個元組的第一個元素
        return [professor[0] for professor in professors]

    except Exception as e:
        print(f"獲取教授名單時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def create_mentorship_request(professor_id, student_id):
    """
    創建指導邀請
    參數：
    professor_id: 教授ID
    student_id: 學生ID

    處理流程：
    1. 在 mentorshiprequest 表中創建新的指導邀請記錄
    2. 設定初始狀態為待回覆 (status = 0)
    3. 記錄當前日期為請求日期

    狀態說明：
    - status = 0: 待回覆
    - status = 1: 同意邀請
    - status = 2: 拒絕邀請
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # SQL 查詢：插入新的指導邀請記錄
        # status = 0 表示待回覆狀態
        # CURDATE() 獲取當前日期作為請求日期
        query = """
            INSERT INTO mentorshiprequest (professorID, studentID, status, requestDate)
            VALUES (%s, %s, 0, CURDATE())
        """
        # 執行 SQL 查詢，插入新記錄
        cursor.execute(query, (professor_id, student_id))

        connection.commit()

    except Exception as e:
        # 發生錯誤時回滾交易
        print(f"創建指導邀請時發生錯誤: {str(e)}")
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# 獲取教授ID
def get_professor_id_by_name(name):
    """
    根據教授姓名獲取其 ID
    參數：
    name: 教授姓名

    返回：
    int: 教授ID (如果找到)
    None: 如果找不到對應的教授
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 查詢指定姓名教授的 ID
        cursor.execute(
            "SELECT professorID FROM professor WHERE name = %s", (name,))
        result = cursor.fetchone()
        # 如果找到教授則返回其 ID，否則返回 None
        return result[0] if result else None

    except Exception as e:
        print(f"查詢教授ID時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def check_existing_student(rankType, rank):
    """
    檢查是否已存在相同考試類型和名次的學生
    參數：
    rankType: 考試類型（如：考試分發、申請入學）
    rank: 名次

    返回：
    bool: True 表示已存在相同條件的學生
         False 表示不存在相同條件的學生
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 查詢符合條件的學生數量
        cursor.execute("""
            SELECT COUNT(*) 
            FROM student 
            WHERE rankType = %s AND rank = %s
        """, (rankType, rank,))
        count = cursor.fetchone()[0]
        # 如果數量大於 0 則表示已存在
        return count > 0

    except Exception as e:
        print(f"檢查學生資料時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def check_existing_account(account):
    """
    檢查帳號是否已存在
    參數：
    account: 要檢查的帳號名稱（通常是電子郵件）

    返回：
    bool: True 表示帳號已存在
         False 表示帳號不存在
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 查詢符合帳號名稱的數量
        cursor.execute("""
            SELECT COUNT(*) 
            FROM account 
            WHERE account = %s
        """, (account,))
        count = cursor.fetchone()[0]
        # 如果數量大於 0 則表示帳號已存在
        return count > 0

    except Exception as e:
        print(f"檢查帳號時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def check_existing_location(location):
    """
    檢查研究室位置是否已被使用
    參數：
    location: 要檢查的研究室位置

    返回：
    bool: True 表示該位置已被使用
         False 表示該位置尚未被使用
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 查詢符合研究室位置的數量
        cursor.execute("""
            SELECT COUNT(*) 
            FROM otherinfo 
            WHERE location = %s
        """, (location,))
        count = cursor.fetchone()[0]
        # 除錯用：印出查詢結果
        print(f"location_count: {count}")
        # 如果數量大於 0 則表示位置已被使用
        return count > 0

    except Exception as e:
        print(f"檢查研究室位置時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def get_student_mentorship_requests(student_id):
    """
    獲取學生的指導邀請記錄
    參數：
    student_id: 學生ID

    返回：
    list: 包含指導邀請記錄的列表，每筆記錄包含：
        - professorName: 教授姓名
        - status: 邀請狀態（待回覆/同意邀請/拒絕邀請）
        - submissionTime: 申請日期 (YYYY-MM-DD格式)
        - reviewTime: 審核日期 (YYYY-MM-DD格式, 若未審核則為'尚未審核')

    排序方式：
    - 按申請日期降序（新的在前）
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 執行 SQL 查詢，獲取學生的指導邀請記錄
        # 查詢包含：教授名字、邀請狀態、申請日期和審核日期
        cursor.execute("""
            SELECT p.name, 
                   CASE m.status 
                       WHEN 0 THEN '待回覆'
                       WHEN 1 THEN '同意邀請'
                       WHEN 2 THEN '拒絕邀請'
                   END as status,
                   m.requestDate,
                   m.approvalDate
            FROM mentorshiprequest m
            JOIN professor p ON m.professorID = p.professorID
            WHERE m.studentID = %s
            ORDER BY m.requestDate DESC  -- 按申請日期降序排列
        """, (student_id,))

        # 處理查詢結果，轉換日期格式
        records = []
        for row in cursor.fetchall():
            records.append({
                'professorName': row[0],
                'status': row[1],
                # 格式化申請日期
                'submissionTime': row[2].strftime('%Y-%m-%d') if row[2] else '',
                # 格式化審核日期
                'reviewTime': row[3].strftime('%Y-%m-%d') if row[3] else '尚未審核'
            })
        return records

    except Exception as e:
        print(f"獲取指導邀請記錄時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def get_student_id_by_account_id(account_id):
    """
    根據帳號ID獲取學生ID
    參數：
    account_id: 帳號ID (來自account表)

    返回：
    int: 學生ID (如果找到)
    None: 如果找不到對應的學生

    說明：
    用於將登入帳號ID轉換為學生ID, 以便進行其他相關操作
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 查詢 student 表中與 accountID 對應的 studentID
        cursor.execute("""
            SELECT studentID 
            FROM student 
            WHERE accountID = %s
        """, (account_id,))
        result = cursor.fetchone()
        # 如果查詢結果存在，返回 studentID，否則返回 None
        return result[0] if result else None

    except Exception as e:
        # 發生錯誤時印出錯誤訊息
        print(f"查詢學生ID時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def get_professor_mentorship_requests(professor_id):
    """
    獲取教授收到的待處理指導請求記錄
    參數：
    professor_id: 教授ID

    返回：
    list: 包含指導請求記錄的列表，每筆記錄包含：
        - name: 學生姓名
        - email: 學生電子郵件
        - rankType: 考試類型（如：考試分發、申請入學）
        - rank: 名次
        - requestDate: 申請日期 (YYYY-MM-DD格式)
        - status: 申請狀態 (0=待回覆）
        - studentID: 學生ID
        - professorID: 教授ID
        - requestID: 指導請求記錄ID

    說明：
    - 只返回狀態為待回覆 (status=0)的請求
    - 按申請日期降序排列（新的在前）
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 查詢待處理的指導請求記錄
        cursor.execute("""
            SELECT 
                s.name,          -- 學生姓名
                s.email,         -- 學生電子郵件
                s.rankType,      -- 考試類型
                s.rank,          -- 名次
                m.requestDate,   -- 申請日期
                m.status,        -- 申請狀態
                s.studentID,     -- 學生ID
                m.professorID,   -- 教授ID
                m.mentorshipRequestID  -- 指導請求記錄ID
            FROM mentorshiprequest m
            JOIN student s ON m.studentID = s.studentID
            WHERE m.professorID = %s AND m.status = 0  -- 只查詢待回覆的請求
            ORDER BY m.requestDate DESC  -- 按申請日期降序排序
        """, (professor_id,))

        # 處理查詢結果
        records = []
        for row in cursor.fetchall():
            records.append({
                'name': row[0],
                'email': row[1],
                'rankType': row[2],
                'rank': row[3],
                # 格式化日期
                'requestDate': row[4].strftime('%Y-%m-%d') if row[4] else '',
                'status': row[5],
                'studentID': row[6],
                'professorID': row[7],
                'requestID': row[8]
            })
        return records

    except Exception as e:
        # 發生錯誤時印出錯誤訊息
        print(f"獲取指導請求記錄時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def update_mentorship_request_status(studentID, professorID, student_name, new_status, request_id):
    """
    更新指導請求的狀態
    參數：
    studentID: 學生ID
    professorID: 教授ID
    student_name: 學生姓名（目前未使用）
    new_status: 新的狀態值
        - 1: 同意邀請
        - 2: 拒絕邀請
    request_id: 指導請求記錄ID

    處理流程：
    1. 更新指導請求的狀態
    2. 設定審核日期為當前日期
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # 更新狀態和審核日期
        cursor.execute("""
            UPDATE mentorshiprequest
            SET status = %s,           -- 更新狀態
                approvalDate = CURDATE()  -- 設定審核日期為當前日期
            WHERE studentID = %s        -- 指定學生
            AND professorID = %s        -- 指定教授
            AND mentorshipRequestID = %s -- 指定請求記錄
        """, (new_status, studentID, professorID, request_id))
        connection.commit()

    except Exception as e:
        # 發生錯誤時回滾交易
        print(f"更新指導請求狀態時發生錯誤: {str(e)}")
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_professor_mentorship_history(professor_id):
    """
    獲取教授的指導邀請歷史記錄
    參數：
    professor_id: 教授ID

    返回：
    list: 包含已處理的指導邀請記錄的列表，每筆記錄包含：
        - name: 學生姓名
        - status: 處理結果（同意邀請/拒絕邀請）
        - approvalDate: 審核日期 (YYYY-MM-DD格式)

    說明：
    - 只返回已處理的請求 (status = 1 或 2)
    - 按審核日期降序排列（新的在前）
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT 
                s.name,                  -- 學生姓名
                CASE m.status 
                    WHEN 1 THEN '同意邀請'  -- 狀態 1 表示同意
                    WHEN 2 THEN '拒絕邀請'  -- 狀態 2 表示拒絕
                END as status,           -- 處理結果
                m.approvalDate           -- 審核日期
            FROM mentorshiprequest m
            JOIN student s ON m.studentID = s.studentID  -- 關聯學生資料
            WHERE m.professorID = %s     -- 篩選特定教授
            AND m.status IN (1, 2)       -- 只查詢已處理的請求
            ORDER BY m.approvalDate DESC -- 按審核日期降序排列
        """, (professor_id,))

        # 處理查詢結果
        records = []
        for row in cursor.fetchall():
            records.append({
                'name': row[0],
                'status': row[1],
                # 格式化日期
                'approvalDate': row[2].strftime('%Y-%m-%d') if row[2] else ''
            })
        return records

    except Exception as e:
        # 發生錯誤時印出錯誤訊息
        print(f"獲取指導邀請歷史記錄時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()


def check_student_mentorship_status(student_id):
    """
    檢查學生是否有待回覆或已同意的指導邀請
    參數：
    student_id: 學生ID

    返回：
    str: 指導邀請的狀態
        - "pending": 有待回覆的邀請 (status = 0)
        - "accepted": 有已同意的邀請 (status = 1)
        - None: 沒有待回覆或已同意的邀請

    說明：
    - 只檢查最新的一筆記錄（使用 LIMIT 1)
    - 只關注待回覆和已同意的狀態 (status IN (0, 1))
    - 用於防止學生同時發送多個指導邀請
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT status 
            FROM mentorshiprequest 
            WHERE studentID = %s         -- 指定學生
            AND status IN (0, 1)         -- 只檢查待回覆(0)和已同意(1)的狀態
            LIMIT 1                      -- 只取最新一筆
        """, (student_id,))
        result = cursor.fetchone()

        if result:
            status = result[0]
            if status == 0:
                return "pending"          # 有待回覆的邀請
            elif status == 1:
                return "accepted"         # 有已同意的邀請
        return None                      # 沒有待回覆或已同意的邀請

    except Exception as e:
        # 發生錯誤時印出錯誤訊息
        print(f"檢查學生指導狀態時發生錯誤: {str(e)}")
        raise

    finally:
        cursor.close()
        connection.close()
