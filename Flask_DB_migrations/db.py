from main import db, Employees

db.create_all()  # sukurs mūsų lentelę DB

# Iš karto inicijuosime testams keletą įrašų:
jonas = Employees('Jonas', 'Jonaitis', 'Programmer')
antanas = Employees('Antanas', 'Antanaitis', 'Analyst')
juozas = Employees('Juozas', 'Juozaitis', 'Accountant')
greta = Employees('Greta', 'Gretaite', 'Programmer')
laura = Employees('Laura', 'Lauraite', 'Accountant')

db.session.add_all([jonas, antanas, juozas, greta, laura])
db.session.commit()

print(jonas.id)
print(antanas.id)
print(juozas.id)
print(greta.id)
print(laura.id)
