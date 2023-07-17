from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog  
import tkinter.messagebox as msgbox
import time, shutil, os, requests
import pandas as pd
from bs4 import BeautifulSoup


root = Tk()
root.title("Coupang Scarpper")
root.geometry("600x500")
root.resizable(False,False)

def coupang_search(keywords,pages):        
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Whale/3.21.192.18 Safari/537.36","Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}
        # headers에 "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3" 를 추가하면 크롤링이 되는데 무슨 의미일까..
    finall = []
    for page in range(1,pages+1):
        url = f"https://www.coupang.com/np/search?q={keywords}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={page}&rocketAll=false&searchIndexingToken=1=9&backgroundColor="
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")

        product_list = soup.find("ul", id='productList').find_all("li")
        for product in product_list:
            a_link = product.find("a")['href']
            pd_link = "https://www.coupang.com" + a_link
            pd_name = product.find("div",attrs={"class":"name"}).get_text().strip()
            try:
                pd_rate = product.find("div",attrs={"class":"rating-star"}).get_text().strip()
                pd_price = product.find("strong",attrs={"class":"price-value"}).get_text()
            except:
                pd_price = "Data_lost"
                pd_rate = "None"
            product_info = (pd_name, pd_link, pd_price, pd_rate)
            finall.append(product_info)            
        
    selectdata = pd.DataFrame(finall, columns=["제품명","링크","가격","평점"])
    file_name = f"crolling_{keywords}_{pages}.csv"
    selectdata.to_csv(r'C:/PythonStudy/Hirae/'+file_name,encoding="cp949", index=False)        


def scrap():
    coupang_search(keyword.get(),int(pages.get()))
    file_name = f"crolling_{keyword.get()}_{pages.get()}.csv"
    time.sleep(1)
    f_path = r"C:/PythonStudy/Hirae/"+file_name
    test_csv = pd.read_csv(f_path,encoding='cp949').values
    for rows in test_csv:
        text_file.insert(END,rows)

def browse_path():
    global idx
    global folder_selected
    folder_selected = filedialog.askdirectory()
    if folder_selected == None:
        return
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0, folder_selected)
    idx=1
    
def save_file():
    global idx
    # keyword, page 입력 안함 오류
    if keyword.get() == "Search" or pages.get() == "Pages":
        msgbox.showerror("오류","검색 키워드와 페이지를 올바르게 입력하세요")
    # 저장경로 없음 오류
    if idx == 0:
        msgbox.showerror("오류","저장경로를 지정해주세요")
        
    opt_type = cmb_save.get() 
    f_name = f"crolling_{keyword.get()}_{pages.get()}.csv"
    f_path = r"C:/PythonStudy/Hirae/"+f_name 
    
    if opt_type == "csv":
        shutil.move(f_path, folder_selected)
    elif opt_type == "txt":
        test_csv = pd.read_csv(f_path,encoding='cp949').values
        with open(f_path.replace(".csv",".txt"), "w") as f:
            for rows in test_csv:
                text = ":".join(rows)
                f.write(text)
        shutil.move(r"C:/PythonStudy/Hirae/"+f_name.replace(".csv",".txt"), folder_selected)

    idx = 0
    msgbox.showinfo("완료","저장되었습니다")

# 저장경로 지정 표시하기 위한 변수
idx = 0

# 키워드, 페이지, 서치 프레임
input_frame = Frame(root, padx=5, pady=5)
input_frame.pack(fill="both")

lbl_keyword = Label(input_frame, text="검색 키워드", width=10)
lbl_keyword.pack(side="left", padx=5,pady=5)
keyword = Entry(input_frame)
keyword.pack(side="left",expand=True,pady=5)
keyword.insert(0,"Search")

lbl_page = Label(input_frame, text="가져올 페이지 수", width=12)
lbl_page.pack(side="left",padx=5,pady=5)
pages = Entry(input_frame)
pages.pack(side="left", expand=True,pady=5)
pages.insert(0,"Pages")

btn_search = Button(input_frame, text="검색", command=scrap)
btn_search.pack(side="right",padx=5,pady=5)

# 텍스트 프레임
text_frame = LabelFrame(root,text="미리보기")
text_frame.pack(fill="both")
# 스크롤바
scrollbar = Scrollbar(text_frame)
scrollbar.pack(side="right",fill="y")

# 텍스트 리스트박스
text_file = Listbox(text_frame,selectmode="extended",height=20,yscrollcommand=scrollbar.set)
text_file.pack(side="left",fill="x",expand=True)
scrollbar.config(command=text_file.yview)


# 저장경로 프레임
dest_frame = LabelFrame(root, text="저장 경로",padx=5,pady=5)
dest_frame.pack(fill="both")
# 찾아보기 버튼
btn_dest = Button(dest_frame, padx=5, pady=10, width=12, text="찾아보기", command=browse_path)
btn_dest.pack(side="right")
# 저장 경로 텍스트
txt_dest_path = Entry(dest_frame)
txt_dest_path.pack(side="left", fill="x", expand=True)

# 옵션 프레임
opt_frame = Frame(root, padx=5, pady=5)
opt_frame.pack(side="left",fill="both")


# 저장 파일 형식 선택
lbl_save_opt = Label(opt_frame, text = "저장 형식", width=10)
lbl_save_opt.pack(side="left", ipadx=5)

opt_save = ["csv","txt"]
cmb_save = ttk.Combobox(opt_frame,state="readonly",values=opt_save, width=7)
cmb_save.current(0)
cmb_save.pack(side="left", ipadx=5)


# 저장/종료 프레임
save_frame = Frame(root,relief="sunken")
save_frame.pack(side="right",fill="both")

btn_save = Button(save_frame, padx=5, pady=5, width=12, text="저장", command=save_file)
btn_cancel = Button(save_frame, padx=5, pady=5, width=12, text="종료", command=root.quit)
btn_cancel.pack(side="right")
btn_save.pack(side="right")




root.mainloop()