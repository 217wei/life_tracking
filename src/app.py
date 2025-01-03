from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# 設定資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///life_tracking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#########################################################
### 定義資料模型
### 新增修改自己負責的部分，這個部分已經寫好的是gpt產生的範例，有幾個還沒完成要自己修改跟新增
### User, HealthData, DietData, SleepData, ExerciseData, goal, medical history
#########################################################

### 待完成
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # 用戶名，必填且唯一
    password = db.Column(db.String(50), nullable=False)               # 密碼，必填
    phone = db.Column(db.String(15), unique=True, nullable=False)     # 電話號碼，必填且唯一
    gender = db.Column(db.String(10), nullable=True)                  # 性別，可選
    birth_date = db.Column(db.Date, nullable=True)                    # 出生日期，可選
    init_weight = db.Column(db.Float, nullable=True)                  # 初始體重，可選，浮點型
    height = db.Column(db.Float, nullable=True)                       # 身高（以公分為單位），可選，浮點型
    
### 待完成
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blood_pressure = db.Column(db.String(20))
    heart_rate = db.Column(db.String(20))
    weight = db.Column(db.Float)

class DietData(db.Model):
    __tablename__ = 'diet_data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

class MedicalHistoryData(db.Model):
    __tablename__ = 'medicalHistory_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    familyHistory = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)
    diseases = db.Column(db.Text, nullable=False)
    
    user = db.relationship('User', backref=db.backref('medical_histories', cascade='all, delete'))

### 待完成
class SleepData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sleep_hours = db.Column(db.Float)
    sleep_quality = db.Column(db.String(20))  # 好/中/差

### 待完成...... 


#建立資料表結構
with app.app_context():
    db.create_all()

#########################################################
### 這裡每一個模塊是大家要分工要寫的
### User, HealthData, DietData, SleepData, ExerciseData, goal, medical history
### 
#########################################################

# 首頁（登入頁面）
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 驗證使用者名稱和密碼
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('dashboard', user_id=user.id))  # 登入成功，傳遞 user_id
        else:
            return "Login failed. Please check your username and password."
    return render_template('home.html')

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        gender = request.form['gender']
        birth_date = request.form['birth_date']
        init_weight = request.form['init_weight']
        height = request.form['height']

        if not phone.isdigit():
            return "Phone number must contain only digits", 400
        
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None # 將 birth_date 轉換為 datetime.date 類型
        
        # 新增使用者
        new_user = User(
            username=username,
            password=password,
            phone=phone,
            gender=gender,
            birth_date=birth_date,
            init_weight=float(init_weight) if init_weight else None,
            height=float(height) if height else None
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))  # 註冊成功後回到登入頁面
    return render_template('register.html')

# 功能頁面
@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    return render_template('dashboard.html', user_id=user_id)


#########################################################
# 新增健康資料
@app.route('/add_health/<int:user_id>', methods=['GET', 'POST'])
def add_health(user_id):
    if request.method == 'POST':
        blood_pressure = request.form['blood_pressure']
        heart_rate = request.form['heart_rate']
        weight = request.form['weight']

        new_health = HealthData(user_id=user_id, blood_pressure=blood_pressure, heart_rate=heart_rate, weight=weight)
        db.session.add(new_health)
        db.session.commit()
        return redirect(url_for('dashboard', user_id=user_id))
    return render_template('add_health.html')

# 查看健康資料
@app.route('/view_health/<int:user_id>')
def view_health(user_id):
    health_data = HealthData.query.filter_by(user_id=user_id).all()
    return render_template('view_health.html', health_data=health_data, user_id=user_id)

# 編輯健康資料
@app.route('/edit_health/<int:health_id>', methods=['GET', 'POST'])
def edit_health(health_id):
    health = HealthData.query.get_or_404(health_id)
    if request.method == 'POST':
        health.blood_pressure = request.form['blood_pressure']
        health.heart_rate = request.form['heart_rate']
        health.weight = request.form['weight']
        db.session.commit()
        return redirect(url_for('view_health', user_id=health.user_id))
    return render_template('edit_health.html', health=health)

# 刪除健康資料
@app.route('/delete_health/<int:health_id>')
def delete_health(health_id):
    health = HealthData.query.get_or_404(health_id)
    user_id = health.user_id
    db.session.delete(health)
    db.session.commit()
    return redirect(url_for('view_health', user_id=user_id))

#########################################################
# 新增飲食資料
@app.route('/add_diet/<int:user_id>', methods=['GET', 'POST'])
def add_diet(user_id):
    if request.method == 'POST':
        # 從表單獲取數據
        meal_type = request.form['meal_type']
        carbs = request.form['carbs']
        fats = request.form['fats']
        protein = request.form['protein']
        calories = (float(carbs) * 4) + (float(fats) * 9) + (float(protein) * 4)
        notes = request.form['notes']

        # 儲存到資料庫
        new_diet = DietData(user_id=user_id, meal_type=meal_type, carbs=carbs, fats=fats, protein=protein, calories=calories, notes=notes)
        db.session.add(new_diet)
        db.session.commit()

        # 重定向到主畫面或其他頁面
        return redirect(url_for('dashboard', user_id=user_id))
    return render_template('add_diet.html', user_id=user_id)


#查看飲食資料
@app.route('/view_diet/<int:user_id>')
def view_diet(user_id):
    # 從資料庫中查詢該用戶的飲食數據
    diet_data = DietData.query.filter_by(user_id=user_id).all()

    # 渲染前端模板
    return render_template('view_diet.html', diet_data=diet_data, user_id=user_id)

#修改飲食資料
@app.route('/edit_diet/<int:diet_id>', methods=['GET', 'POST'])
def edit_diet(diet_id):
    # 查詢要編輯的飲食資料
    diet = DietData.query.get_or_404(diet_id)

    if request.method == 'POST':
        # 從表單獲取更新的數據
        diet.meal_type = request.form['meal_type']
        diet.carbs = float(request.form['carbs'])
        diet.fats = float(request.form['fats'])
        diet.protein = float(request.form['protein'])
        diet.calories = (diet.carbs * 4) + (diet.fats * 9) + (diet.protein * 4)
        diet.notes = request.form['notes']

        # 更新到資料庫
        db.session.commit()

        # 重定向到查看飲食數據的頁面
        return redirect(url_for('view_diet', user_id=diet.user_id))

    # 初始加載編輯頁面
    return render_template('edit_diet.html', diet=diet)

#刪除飲食資料
@app.route('/delete_diet/<int:diet_id>', methods=['POST'])
def delete_diet(diet_id):
    diet = DietData.query.get_or_404(diet_id)
    user_id = diet.user_id
    db.session.delete(diet)
    db.session.commit()
    flash('Diet record deleted successfully!', 'success')
    return redirect(url_for('view_diet', user_id=user_id))


#########################################################
# 新增睡眠資料(gpt產生的範例)
@app.route('/add_sleep/<int:user_id>', methods=['GET', 'POST'])
def add_sleep(user_id):
    if request.method == 'POST':
        sleep_hours = request.form['sleep_hours']
        sleep_quality = request.form['sleep_quality']

        new_sleep = SleepData(user_id=user_id, sleep_hours=sleep_hours, sleep_quality=sleep_quality)
        db.session.add(new_sleep)
        db.session.commit()
        return redirect(url_for('dashboard', user_id=user_id))
    return render_template('add_sleep.html')

#########################################################
# 新增醫療歷史記錄
@app.route('/add_medicalHistory/<int:user_id>', methods=['GET', 'POST'])
def add_medicalHistory(user_id):
    if request.method == 'POST':
        # 從表單獲取數據
        familyHistory = request.form['familyHistory']
        allergies = request.form['allergies']
        diseases = request.form['diseases']

        # 儲存到資料庫
        new_history = MedicalHistoryData(
            user_id=user_id,
            familyHistory=familyHistory,
            allergies=allergies,
            diseases=diseases
        )
        
        #db.session.add(new_history)
        #db.session.commit()
        
        try:
            db.session.add(new_history)
            db.session.commit()
            # 提示並重定向
            flash('Medical history added successfully!', 'success')
            return redirect(url_for('dashboard', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", 'danger')
            return redirect(url_for('add_medicalHistory', user_id=user_id))

    return render_template('add_medicalHistory.html', user_id=user_id)

# 查看醫療歷史記錄
@app.route('/view_medicalHistory/<int:user_id>')
def view_medical_history(user_id):
    # 查詢該用戶的醫療歷史記錄
    medicalHistory = MedicalHistoryData.query.filter_by(user_id=user_id).all()

    # 如果找不到資料，回傳提示
    #if not medicalHistory:
    #    flash('No medical history found for this user.', 'warning')
    #    return redirect(url_for('dashboard', user_id=user_id))
    
    # 渲染模板
    return render_template('view_medicalHistory.html', medicalHistory =medicalHistory , user_id=user_id)

# 修改醫療歷史記錄
@app.route('/edit_medicalHistory/<int:history_id>', methods=['GET', 'POST'])
def edit_medicalHistory(history_id):
    # 查詢要編輯的記錄
    history = MedicalHistoryData.query.get_or_404(history_id)

    if request.method == 'POST':
        # 從表單獲取更新數據
        history.familyHistory = request.form['familyHistory']
        history.allergies = request.form['allergies']
        history.diseases = request.form['diseases']

        # 更新到資料庫
        db.session.commit()

        # 提示並重定向
        flash('Medical history updated successfully!', 'success')
        return redirect(url_for('view_medical_history', user_id=history.user_id))

    return render_template('edit_medicalHistory.html', history=history)

# 刪除醫療歷史記錄
@app.route('/delete_medicalHistory/<int:history_id>', methods=['POST'])
def delete_medical_history(history_id):
    # 查詢記錄
    medicalHistory= MedicalHistoryData.query.get_or_404(history_id)
    user_id = medicalHistory.user_id

    # 刪除資料庫記錄
    db.session.delete(medicalHistory)
    db.session.commit()

    # 提示並重定向
    flash('Medical history deleted successfully!', 'success')
    return redirect(url_for('view_medical_history', user_id=user_id))

#########################################################
### 待完成...... 




#########################################################
if __name__ == '__main__':
    app.run(debug=True)