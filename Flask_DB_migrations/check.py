from main import db, Employees


def get_all_employees():
    print(Employees.query.all())


def add_employee_age(num: int, age: int):
    employee = Employees.query.get(num)
    employee.age = age
    db.session.add(employee)
    db.session.commit()
    print(Employees.query.all())


def add_employee_email(num: int, email: str):
    employee = Employees.query.get(num)
    employee.email_address = email
    db.session.add(employee)
    db.session.commit()
    print(Employees.query.all())


# add_employee_age(1, 30)
# add_employee_age(4, 25)
# add_employee_email(1, 'jonas@gmail.com')
# add_employee_email(2, 'antanas@gmail.com')
# add_employee_email(5, 'laural@gmail.com')
get_all_employees()


