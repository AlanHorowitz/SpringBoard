import requests
import time

img_lst = [
"https://images.unsplash.com/photo-1591444539769-2518e73d1090",
"https://images.unsplash.com/photo-1552770687-655f35ecf8b4",
"https://images.unsplash.com/photo-1529686398651-b8112f4bb98c",
"https://images.unsplash.com/photo-1488459716781-31db52582fe9",
"https://images.unsplash.com/photo-1590502160462-58b41354f588",
"https://images.unsplash.com/photo-1603573355706-3f15d98cf100",
"https://images.unsplash.com/photo-1554939437-ecc492c67b78",
"https://images.unsplash.com/photo-1549643276-fdf2fab574f5",
"https://images.unsplash.com/photo-1600310590439-e493a073d1ad",
"https://images.unsplash.com/photo-1543007168-5fa9b3c5f5fb",
"https://images.unsplash.com/photo-1529768167801-9173d94c2a42"
]

# read files from web and write to temp directory
def get_files_nothreads(img_lst, ctr=0):
    
    i = ctr
    for url in img_lst:
        r = requests.get(url)
        if r.status_code != 200:
            print(f'status code not 200 was: {r.status_code}')
        else:
            with open("tmp/img_unsplash_"+str(i)+".jpg", "wb") as file:
                file.write(r.content)
                i += 1
    return i
    # TODO make and delete folder


import threading
def get_files_threads_1(img_lst):
    mid = len(img_lst) // 2
    img_lst_1 = img_lst[:mid]
    img_lst_2 = img_lst[mid:]

    t1 = threading.Thread(target=get_files_nothreads,args=(img_lst_1,), kwargs={'ctr': 0})
    t2 = threading.Thread(target=get_files_nothreads,args=(img_lst_2,), kwargs= {'ctr': mid})
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return len(img_lst)   # not easy to get return value from thread


start = time.perf_counter()
i = get_files_nothreads(img_lst)
end = time.perf_counter()
print(f'{i} files written in {round(end - start,2)} second(s)')

start = time.perf_counter()
i = get_files_threads_1(img_lst)
end = time.perf_counter()
print(f'{i} files written in {round(end - start,2)} second(s)')
