import numpy as np
# import pandas as pd
import pymysql
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import keras


root1=Tk()
root1.geometry('1200x900')
main = "Restaurant Review Analysis System/"
root1.title(main+"Welcome Page")
root1.config(bg='dark gray')

foods = ["Idly", "Dosa", "Vada", "Roti", "Meals", "Veg Biryani",
         "Egg Biryani", "Chicken Biryani", "Mutton Biryani",
         "Ice Cream", "Noodles", "Manchooriya", "Orange juice",
         "Apple Juice", "Pineapple juice", "Banana juice"]



def take_review():
    root2 = Toplevel()
    root2.geometry('1400x900')
    root2.title(main + "give review")

    label = Label(root2, text="RESTAURANT REVIEW ANALYSIS SYSTEM",
                  bd=2, font=('Arial', 47, 'bold', 'underline'))

    req1 = Label(root2, text="Select the item(s) you have taken.....")

    chk_btns = []
    selected_foods = []
    req2 = Label(root2, text="Give your review below....")
    rev_tf = Entry(root2, width=100, fg='red', borderwidth=5, font=('times new roman', 14, 'bold'))
    req3 = Label(root2, text="NOTE : Use not instead of n't.",
                 font=('times new roman', 12, 'bold'))
    global req4
    req4 = Label(root2, text="Review is ",
                 height=4, width=20, bg='skyblue', font=('times new roman', 14, 'bold'))
    global variables
    variables = []
    chk_btns = []

    for i in range(len(foods)):
        var = IntVar()
        chk = Checkbutton(root2, text=foods[i], variable=var)
        variables.append(var)
        chk_btns.append(chk)

    label.grid(row=0, column=0, columnspan=4)
    req1.grid(row=1, column=0, columnspan=4)
    # req4.grid(row=1,column=0,columnspan=6)
    req1.config(font=("Helvetica", 30))

    for i in range(4):
        for j in range(4):
            c = chk_btns[i * 4 + j]
            c.grid(row=i + 3, column=j, columnspan=1, sticky=S)

    submit_review = Button(root2, text="Submit Review", font=(
        'Arial', 20), padx=100, pady=20, command=lambda: [
        estimate(rev_tf.get())])

    req2.grid(row=7, column=0, columnspan=4, sticky=W + E)
    req2.config(font=("Helvetica", 20))
    rev_tf.grid(row=8, column=1, rowspan=3, columnspan=2, sticky=S)
    req3.grid(row=11, column=1, columnspan=2)
    submit_review.grid(row=12, column=0, columnspan=4)
    req4.grid(row=12, column=2, columnspan=4)



def estimate(s):
    if s == '':
        messagebox.showinfo('info', 'please give feedback ')
        take_review()
    else:
        s = s.lower()
        f1=open('cv_pickle','rb')
        cv=pickle.load(f1)
        f1.close()
        model=keras.models.load_model('review_RNN_model.keras')
        data=[s]
        data_cv = cv.transform(data).toarray()
        new1=data_cv.reshape(data_cv.shape[0], 1, data_cv.shape[1])
        prediction = model.predict(new1)
        prediction=prediction[0]
        print(prediction)
        if prediction>0.5:
            prediction=1
        else:
            prediction=0
        if ("not" in s) or ("no" in s) or ("n't" in s):
            prediction= abs(prediction - 1)
        if prediction == 0:
            res1 = 'Bad review'
        else:
            res1 = 'Good review'
        req4.config(text=res1)
        # logic of count
        selected_foods = []
        for i in range(len(foods)):
            if variables[i].get() == 1:
                selected_foods.append(foods[i])
        #print(selected_foods)
        conn = pymysql.connect(user='root', password='Tanmay..7920',
                                       host='localhost', database='project1')
        qur = 'select * from rest_table'
        mycur = conn.cursor()
        mycur.execute(qur)
        total = mycur.fetchall()
        # print(total)
        for i in total:
            food1 = list(i)
            if food1[0] in selected_foods:
                food_name = food1[0]
                c = food1[3] + 1
                p = food1[1]
                n = food1[2]
                if prediction == 1:
                    p = p + 1
                else:
                    n = n + 1
                conn = pymysql.connect(user='root', password='Tanmay..7920',
                                               host='localhost', database='project1')
                qur = f'UPDATE rest_table SET good_review={p},bad_review={n},customer={c} WHERE food="{food_name}"'
                mycur = conn.cursor()
                mycur.execute(qur)
                conn.commit()
                mycur.close()
                conn.close()
        selected_foods = []

def login():
    pass


label = Label(root1, text="RESTAURANT REVIEW ANALYSIS SYSTEM",
              bd=2, font=('Arial', 30, 'bold', 'underline'))

ques = Label(root1, text="Are you a Customer or Owner ???")

cust = Button(root1, text="Customer Click Here", bd=5, relief='ridge', font=('Arial', 20),
              padx=30, pady=20, command=take_review)

owner = Label(root1, text="Owner Login here >>>", bd=5, relief='ridge', font=('Arial', 20),
              padx=30, pady=20)
a1 = StringVar()
a2 = StringVar()

lbl1 = Label(root1, text="Owner Username", bd=5, width=20, height=2, relief='ridge', font=('Arial', 12))
lbl2 = Label(root1, text="Password", bd=5, width=20, height=2, relief='ridge', font=('Arial', 12))
e1 = Entry(root1, bd=5, width=14, textvariable=a1, relief='ridge', font=('Arial', 20))
e2 = Entry(root1, bd=5, width=14, textvariable=a2, relief='ridge', font=('Arial', 20), show='*')
owner_l = Button(root1, text="Login", font=('Arial', 20), command=login)

label.grid(row=0, column=0)
ques.grid(row=1, column=0, sticky=W + E)
ques.config(font=("Helvetica", 30))
cust.grid(row=2, column=0)
owner.grid(row=3, column=0)
lbl1.place(x=800, y=230)
lbl2.place(x=800, y=280)
e1.place(x=1000, y=230)
e2.place(x=1000, y=280)
owner_l.place(x=1100, y=340)





root1.mainloop()