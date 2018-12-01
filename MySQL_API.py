import mysql.connector


def search_by_word(word):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="LearMore!0922",
        auth_plugin='mysql_native_password',
        database="mini_project_3"
    )
    mycursor = mydb.cursor()
    # -------------------------------------------
    result = []
    for i in range(10):
        myresult = None
        sql = "SELECT * FROM customers WHERE descriptor" + str(i) + " = '" + word + "'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if myresult is not None:
            for x in myresult:
                result.append(x)
        if not result:
            result.append("There is no such key words")
    return result


def num_of_image(name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="LearMore!0922",
        auth_plugin='mysql_native_password',
        database="mini_project_3"
    )
    mycursor = mydb.cursor()
    myresult = None
    # -------------------------------------------
    sql = "SELECT * FROM customers WHERE user ='" + name + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    number = None
    if myresult is None:
        print("there is no such user")
    else:
        number = myresult[0][2]
    return number


def most_popular_des():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="LearMore!0922",
        auth_plugin='mysql_native_password',
        database="mini_project_3"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customers")
    myresult = mycursor.fetchall()
    result = {}
    for x in myresult:
        for des in x[4:]:
            if des in result.keys():
                result[des] = result[des] + 1
            else:
                result[des] = 0
    a = max(result, key=lambda k: result[k])
    return a



def main():
    word = input("input the word you want to search: ")
    result = search_by_word(word)
    print("the word you search: ", word)
    print("result: ")
    for x in result:
        print(x)
    # ---------------------------
    name = input("input the user name: ")
    number = num_of_image(name)
    print("the number of image this feed is: ", number)
    # ---------------------------
    res = most_popular_des()
    print("the most popular descriptor is: ", res)
    pass


if __name__ == '__main__':
    main()
