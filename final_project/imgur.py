import pyimgur
def imgur_url(user_id):
    CLIENT_ID = "9345c5d096864df"
    PATH = f'pic/{user_id}.png'

    im = pyimgur. Imgur (CLIENT_ID)
    uploaded_image = im.upload_image (PATH, title="name_any")
    print(uploaded_image.link)
    return(uploaded_image.link)