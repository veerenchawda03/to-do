from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#here we define the table, DDL
#the table name is automatically set for you unless overridden. 
# It’s derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”
#Hence this table's name is to_do
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def home_page():

    #if we get a POST from FE, we will take the title from the request and store in title variable, same for desc, then we will create an instance
    #of the db class called todo and then pass it the 2 values, then we add those changes to the db,
    #there in jinja we are running a forloop to increase the sno and display the values in html table from line 43-46 of index.html
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        todo.date_created = datetime.now()
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('home.html', allTodo=allTodo) #here we will render the home page and the query results stored in allTodo on line 32.



@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.updated_at = datetime.now()
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() #in SQLAlchemy, Query.first() returns the first of a potentially larger result set (adding LIMIT 1 to the query)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)