import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mini_project_3_MongoDB"]
# mycol = mydb["customers"]

# for x in mycol.find():
#     print(x)


def find_session_with_word(word, mycol):

    result_final = []
    for x in mycol.find():
        image_number = x['image_number']
        result_per = []
        for i in range(image_number):
            lowered_name = "image"+str(i)
            result = None
            for label in x["image_info"][lowered_name]["descriptors"]:
                if word == label:
                    result = {
                        "_id": x["_id"],
                        "name": x["name"],
                        "image": lowered_name,
                        "url": x["image_info"][lowered_name]["url"],
                        "descriptors": x["image_info"][lowered_name]["descriptors"]
                    }
                    break
            if result is not None:
                result_per.append(result.copy())
                # print(result)
        if result_per:
            result_final.append(result_per.copy())
    return result_final


def num_of_image(mycol):
    output_final = []
    for x in mycol.find():
        output = {
            "_id": x["_id"],
            "time": x["time"],
            "name": x["name"],
            "number_of_image": x["image_number"]
        }
        output_final.append(output)
    return output_final


def most_popular_des(mycol):
    result = {}
    for x in mycol.find():
        image_number = x['image_number']
        for i in range(image_number):
            lowered_name = "image" + str(i)
            for label in x["image_info"][lowered_name]["descriptors"]:
                if label in result.keys():
                    result[label] = result[label] + 1
                else:
                    result[label] = 0
    a = max(result, key=lambda k: result[k])
    # print("The most popular descriptors is ", a)
    return a


def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mini_project_3_MongoDB"]
    mycol = mydb["customers"]
    word = input("input the word you want to search")
    search = find_session_with_word(word, mycol)
    print(search)
    number = num_of_image(mycol)
    print(number)
    a = most_popular_des(mycol)
    print("The most popular descriptors is ", a)


if __name__ == '__main__':
    main()
