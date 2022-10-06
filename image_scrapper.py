import time
from selenium import webdriver
import requests
import os

def scroll_to_down(wd):
    wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)


def url_collecting_fun(wd,search_term,max_images,search_link):
    wd.get(search_link)
    print('Opened the webpage of {q}'.format(q=search_link))
    time.sleep(2)
    thumbnail_starting_index = 0
    actual_images = set()
    while len(actual_images)<max_images:
        scroll_to_down(wd)
        thumbnails = wd.find_elements('css selector', 'img.rg_i.Q4LuWd')
        number_of_thumbnails_found=len(thumbnails)-thumbnail_starting_index
        print('Found {q} number of images'.format(q=number_of_thumbnails_found))
        # print('Saving the links of images now!!!!')
        print('Saving the links of images from index {a} to {b}'.format(a=thumbnail_starting_index, b=len(thumbnails)))
        for thumbnail in thumbnails[thumbnail_starting_index:len(thumbnails)]:
            try:
                thumbnail.click()
                time.sleep(2)  # let the image load after clicking and then search for img tag. Else it won't be registered
                new = wd.find_elements('css selector', 'img.n3VNCb.KAlRDb')
                if new[0].get_attribute('src') and 'https' in new[0].get_attribute('src'):
                    actual_images.add(new[0].get_attribute('src'))
                    print('Added URL of Image number {q}'.format(q=len(actual_images)))
                    if len(actual_images)>=max_images:
                        time.sleep(2)
                        print('Done saving the links!!!!!')
                        break #breaks out of thumbnail for loop
            except Exception as e:
                print(e)
        print('Saved the links of {q} images'.format(q=len(actual_images)))
        if len(actual_images)<max_images:
            print('Looking for ',max_images-len(actual_images),' more images.....')
            thumbnail_starting_index=len(actual_images)

    downloading_fun(search_term,actual_images,max_images)


def downloading_fun(search_term,actual_images,max_images):
    print("Started the downloadinng function........")
    directory = r'C:\Users\Darshan Pradeep\Desktop\Practice\images'
    folder_path = os.path.join(directory, '_'.join(
        search_term.lower().split(' ')))  # creating a new folder with the name of search term
    # separated by _
    folder_path  # this is the folder where the photos will be downloaded
    if not os.path.exists(folder_path):  # if the above folder is not present, make a new one
        os.makedirs(folder_path)
    print('Created the folder path successfully !!!!!')
    count = 1
    for image_links in actual_images:  # selecting every image link inside the list one by one
        image_in_bytes = requests.get(
            image_links).content  # reading the images from the files. After this, the image is stored as bytes
        f = open(os.path.join(folder_path, (str(count) + '.png')),
                 'wb')  # opening a new file in write bytes mode to write the bytes of image
        # in side the file. We are saving the file in .png format. So automatically, those bytes will be converted into it's
        # corresponding images
        f.write(image_in_bytes)
        f.close()
        print('Saved image number {q}'.format(q=count))
        count += 1

    print('All images saved. Well done  for saving {q} images'.format(q=count-1))
    print('Number of images still required={q}'.format(q=max_images-count+1))


def first_fun():
    driver_path = r'C:\Users\Darshan Pradeep\Desktop\Practice\chromedriver.exe'
    wd = webdriver.Chrome(driver_path)
    search_term = "sachin tendulkar"
    max_images = 200
    link = "https://www.google.com/search?q={q}&rlz=1C1CHBF_enIN1023IN1023&sxsrf=ALiCzsbmglTijOEFhVZL7i-nj1CAwc-erQ:1665047486859&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjo2fOfocv6AhUi2DgGHVbHBTkQ_AUoAXoECAMQAw&biw=1536&bih=722&dpr=1.25"
    search_link = link.format(q=search_term.replace(' ', '+'))
    print("Search link created!! Collecting URL's now.......")
    url_collecting_fun(wd,search_term,max_images,search_link)

first_fun()


