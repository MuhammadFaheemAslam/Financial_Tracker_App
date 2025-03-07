from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
from .models import User, Budget, Expense, Category
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy.sql import func

bp = Blueprint('main', __name__)
local_tz = timezone('US/Central')

# Home Route
@bp.route('/')
def home():
    return render_template('index.html')

# User Registration
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('main.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# User Login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html')

# Logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.login'))


# View Budgets
@bp.route('/view_budgets', methods=['GET'])
@login_required
def view_budgets():
    budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.year.desc(), Budget.month.desc()).all()

    return render_template('view_budgets.html', budgets=budgets)


# Set Budget (Create New Budget)
@bp.route('/set_budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        period = request.form.get('period')  
        budget_month = int(request.form.get('budget_month'))
        budget_year = int(request.form.get('budget_year'))

        existing_budget = Budget.query.filter_by(
            user_id=current_user.id, period=period, month=budget_month, year=budget_year
        ).first()

        if amount < 0:
            flash('Budget cannot be Negative', 'warning')
            return redirect(url_for('main.set_budget'))
        
        if existing_budget:
            flash(f'Budget already exists for {months[budget_month-1]} {budget_year}. Please update it.', 'danger')
            return redirect(url_for('main.view_budgets'))

        new_budget = Budget(
            user_id=current_user.id, amount=amount, period=period,
            month=budget_month, year=budget_year
        )
        db.session.add(new_budget)
        db.session.commit()
        flash(f'{period.capitalize()} budget set successfully for {months[budget_month-1]} {budget_year}!', 'success')
        return redirect(url_for('main.view_budgets'))

    current_year = 2025 
    years = [current_year, current_year + 1, current_year + 2]

    return render_template('set_budget.html', months=months, years=years)


#edit budget
@bp.route('/edit_budget/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
              'August', 'September', 'October', 'November', 'December']
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()

    if not budget:
        flash('Budget not found or access denied.', 'danger')
        return redirect(url_for('main.view_budgets'))

    if request.method == 'POST':
        try:
            amount = float(request.form['amount']) 
            period = request.form['period']
            budget_month = int(request.form['budget_month'])  
            budget_year = int(request.form['budget_year'])

            budget.amount = amount
            budget.period = period
            budget.month = budget_month
            budget.year = budget_year

            db.session.commit()
            flash(f'{period.capitalize()} budget updated successfully for {months[budget_month-1]} {budget_year}!', 'success')
            return redirect(url_for('main.view_budgets'))

        except (ValueError, TypeError):
            flash("Invalid input. Please check your values.", "danger")

    current_year = datetime.now().year
    years = list(range(current_year, current_year + 3))

    return render_template('edit_budget.html', months=months, years=years, budget=budget)


# Delete Budget
@bp.route('/delete_budget/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    if budget.user_id != current_user.id:
        flash('You cannot delete someone else\'s budget.', 'danger')
        return redirect(url_for('main.view_budgets'))

    db.session.delete(budget)
    db.session.commit()
    flash('Budget deleted successfully!', 'success')

    return redirect(url_for('main.view_budgets'))



# Add Category
@bp.route('/add_category', methods=['POST'])
@login_required
def add_category():
    category_name = request.form['category_name']
    existing_category = Category.query.filter_by(name=category_name).first()

    if existing_category:
        flash('Category already exists', 'danger')
    else:
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully', 'success')

    return redirect(url_for('main.add_expense'))



# Add Expense
@bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    categories = Category.query.all()

    if request.method == 'POST':
        category_id = request.form.get('category')
        amount = float(request.form.get('amount'))
        description = request.form.get('description')
        expense_date = request.form.get('expense_date')  
        
        if amount < 0:
            flash("Amount cannot be negative", "danger")
            return redirect(url_for('main.add_expense'))
        if not category_id:
            flash("Please select a category", "danger")
            return redirect(url_for('main.add_expense'))
        if expense_date:
            expense_date = datetime.fromisoformat(expense_date)  
        else:
            expense_date = datetime.now()  

        new_expense = Expense(user_id=current_user.id,
                              category_id=category_id,
                              amount=amount,
                              description=description,
                              date=expense_date)

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_expense.html', categories=categories)


#view expenses
@bp.route('/expenses')
@login_required
def view_expenses():
    month = request.args.get('month', None, type=int)  
    year = request.args.get('year', None, type=int) 
    selected_category = request.args.get('category', None, type=int)  
    order_by = request.args.get('order_by', 'date')  
    current_year = datetime.now().year

    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    expenses = Expense.query.filter(Expense.user_id == current_user.id)
    if month:
        expenses = expenses.filter(func.extract('month', Expense.date) == month)
    if year:
        expenses = expenses.filter(func.extract('year', Expense.date) == year)
    if selected_category:
        expenses = expenses.filter(Expense.category_id == selected_category)

    if order_by == 'category':
        expenses = expenses.join(Expense.category).order_by(Category.name.asc())
    else:
        expenses = expenses.order_by(Expense.date.desc())  
    expenses = expenses.all()

    for expense in expenses:
        expense.date = expense.date.astimezone(local_tz)

    categories = Category.query.all()

    return render_template(
        'expenses.html',
        expenses=expenses,
        month=month,
        year=year,
        order_by=order_by,
        months=months,
        current_year=current_year,
        categories=categories,
        selected_category=selected_category
    )



@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    today = datetime.utcnow()  

    monthly_budget = Budget.query.filter_by(user_id=current_user.id, period="monthly", month=current_month, year=current_year).first()
    monthly_budget_amount = monthly_budget.amount if monthly_budget else 0

    total_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        func.extract('month', Expense.date) == current_month,
        func.extract('year', Expense.date) == current_year
    ).scalar() or 0

    remaining_monthly_budget = round(monthly_budget_amount - total_expenses,2)
    remaining_budget_percentage = round((remaining_monthly_budget / monthly_budget_amount) * 100) if monthly_budget_amount > 0 else 0

    category_expenses = db.session.query(Category.name, func.sum(Expense.amount)).join(Expense).filter(
        Expense.user_id == current_user.id,
        func.extract('month', Expense.date) == current_month,
        func.extract('year', Expense.date) == current_year
    ).group_by(Category.name).all()

    category_expenses_data = [{"category": category, "total": total} for category, total in category_expenses]


    last_7_days_expenses = db.session.query(func.extract('day', Expense.date), func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.date >= today - timedelta(days=7),  
        Expense.date <= today
    ).group_by(func.extract('day', Expense.date)).all()

    last_7_days_expenses_data = [{"day": int(day), "total": total} for day, total in last_7_days_expenses]


    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1

    last_month_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        func.extract('month', Expense.date) == last_month,
        func.extract('year', Expense.date) == last_month_year
    ).scalar() or 0

    expense_percentage = round((total_expenses / monthly_budget_amount) * 100) if monthly_budget_amount > 0 else 0

    # Fetch the last 5 expenses
    last_5_expenses = db.session.query(Expense).filter_by(user_id=current_user.id).order_by(Expense.date.desc()).limit(5).all()
    last_5_expenses_data = [{
        'description': expense.description,
        'amount': expense.amount,
        'category': expense.category,
        'date': expense.date.astimezone(local_tz)
    } for expense in last_5_expenses]

    return render_template("dashboard.html",
                           monthly_budget=monthly_budget_amount,
                           total_expenses=total_expenses,
                           remaining_budget=remaining_monthly_budget,
                           remaining_budget_percentage=remaining_budget_percentage,
                           category_expenses=category_expenses_data,
                           daily_expenses=last_7_days_expenses_data,  
                           expense_percentage=expense_percentage,
                           last_month_expenses=last_month_expenses,
                           current_month=current_month,
                           current_year=current_year,
                           last_month=last_month,
                           last_month_year=last_month_year,
                           last_5_expenses=last_5_expenses_data)  
