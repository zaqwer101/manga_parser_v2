import requests, os

manga_name = "black_lagoon"
image_server_url = "https://img3.mangalib.me"

def get_page(volume, chapter, page):
    status = False
    if page < 10:
        page = "0" + str(page)
    else:
        page = str(page)

    directory = manga_name + "/volume_" + str(volume) + "/chapter_" + str(chapter) + "/"
    file = directory + page + ".png"

    if os.path.exists(file):
        return True

    page_url = image_server_url + "/manga/" \
               + manga_name \
               + "/chapters/" \
               + str(volume) + "-" + str(chapter) \
               + "/" + page + ".png"
    content = requests.get(page_url).content
    if content == b'':                              # если такой страницы нет
        page_url = image_server_url + "/manga/" \
               + manga_name \
               + "/chapters/" \
               + str(volume) + "-" + str(chapter) \
               + "/" + page + ".jpg"                # пробуем получить jpg версию
        content = requests.get(page_url).content
        if content == b'':   # если и её нет
            status = False
        else:
            status = True
    else:
        status = True

    if status:
        if not os.path.isdir(directory):
            os.makedirs(directory)
        open(file, "wb").write(content)
        print(file)
        return True
    else:
        return False

volume  = 1
chapter = 1
page    = 1

was_special = False
while True:
    while True:
        while True:
            status = get_page(volume, chapter, page)
            if status:
                page += 1
            else:
                break
        # if get_page(volume, chapter + 1, page = 1):

        # попробуем получить special-главу
        if get_page(volume, chapter + 0.5, page = 1):
            chapter += 0.5
            page = 2
        else:
            if (chapter / 0.5) % 2 != 0: # если в прошлую итерацию получали спешуал
                chapter += 0.5
                chapter = int(chapter)
                page = 2 # потому что get_page уже скачал 1 страницу
                was_special = True
            else:
                if get_page(volume, chapter + 1, page = 1): # есть ли ещё главы в этом томе
                    if not was_special:
                        chapter += 1
                    was_special = False
                    page = 2
                else:
                    if not was_special: # потому что в секции для special делается += 0.5 :/
                        chapter += 1
                    was_special = False
                    break
        # else:
        #     chapter += 1
        #     break
    if get_page(volume + 1, chapter, page = 1):
        volume += 1
        page = 2
    else:
        break

print("Done")


