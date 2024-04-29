from flask import Flask, render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///bbau.db"
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

name_of_user=None

class UserData(db.Model):
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),primary_key=True)
    password=db.Column(db.String(30),nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.name}-{self.email}-{self.password}"

class Review(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    review=db.Column(db.String(500))
    
    def __repr__(self) -> str:
        return f"{self.review}"
    

@app.route('/')
def first_fun():
    return render_template("index.html",name_of_user=name_of_user)

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method=="POST":
        user_name=request.form['username']
        user_email=request.form['email']
        passwd=request.form['passwd']
        global name_of_user
        try:
            data1=UserData(name=user_name,email=user_email,password=passwd)
            db.session.add(data1)
            db.session.commit()
            name_of_user=user_name
            return redirect("/",name_of_user=name_of_user)
        except:
            return render_template("signup.html",err_id=1,name_of_user=name_of_user)
    return render_template("signup.html",err_id=0,name_of_user=name_of_user)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['passwd']
        data1=UserData.query.filter_by(email=email).first()
        global name_of_user
        try:
            if data1.password!=password:
                return render_template('login.html',err_id=2,name_of_user=name_of_user)
            else:
                name_of_user=data1.name
                return redirect("/")
        except:
            return render_template('login.html',err_id=1,name_of_user=name_of_user)
    return render_template('login.html',err_id=0,name_of_user=name_of_user)

@app.route('/logout')
def logout():
    global name_of_user
    name_of_user=None
    return redirect('/')


if __name__=="__main__":

    app.run(debug=True)
