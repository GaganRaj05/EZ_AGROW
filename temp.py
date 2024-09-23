file_path = "./static/images/axis.png"
with open(file_path, "rb") as file:
    binary_data = file.read()
    print(binary_data)
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)

cursor.execute("UPDATE PRODUCT_DETAILS SET image=%s, mime_type=%s WHERE product_id=%s", 
               (binary_data, mime_type, 1012))
mysql.connection.commit()