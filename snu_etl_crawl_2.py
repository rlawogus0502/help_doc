# 강의 페이지 : http://etl.snu.ac.kr/course/view.php?id=197170
# 로그인 필요함.

# 로그인 페이지 : https://etl.snu.ac.kr/login.php
# 보통 로그인 API를 찾거나 로그인 하는 것처럼 requests.post를 보낸 후 리턴되는 값을 파악하여 사용. 보통 response header set-cookie에 정보가 있음

# 이 경우는 그냥 브라우저에서 사용하는 값을 써도 되기 때문에 브라우저 값 가져옴
# 웹 로그인 request header 에 있는 정보 사용. 
# 보통 쿠키에 인증값이 들어가며 expire 시간 설정이 되어 있음

import requests, re, os, m3u8,subprocess
import webbrowser
from lxml import html
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import filedialog
import webbrowser

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Host': 'etl.snu.ac.kr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Origin': 'https://sso.snu.ac.kr',
}

#headers['Cookie'] ="InitechEamUIP=RAkH0oSEjHpXV5ndkRTArg%3D%3D; InitechEamUTOA=1; InitechEamUPID=0498wlXpW%2FZWUIVyUDO1cA%3D%3D; _ga=GA1.3.2010195696.1627214885; _gid=GA1.3.33645146.1627214885; ubboard_read=%25A7%2504%25DC%2593%25BD%257BSM%253A%25987%25DA.%2594E4%25B0o%25EC%252A%25FA%2522%25EF%2594x%2523%25A0%25AB; SITicket=DUMMY; InitechEamUID=v199GZ435MtB68fVF9W0mQ%3D%3D; InitechEamULAT=1627223023; InitechEamUHMAC=tyCMfHP%2FpcsTpS2vCPEhdDMfP1qBiu7BwqTyF9UiwBk%3D; MoodleSessionnewetlcm=e1ivgmtt4g6mchd3arieqjnei1; _gat=1"



def main():
    def get_cookie(username, password):
        login_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Host': 'sso.snu.ac.kr',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Origin': 'https://etl.snu.ac.kr',
        'Referer': 'https://etl.snu.ac.kr/'
        }
        
        # 너희 학교는 2단계로 로그인함.
        # 이런경우 session 으로 처리하는게 수동으로 뭔가를 안해도 되서 편함.
        # 예) set-cookie response를 받는 경우 session.request시 cookie가 자동 설정됨.
        session = requests.Session()
        # 이 주소는 login.php html form 에 있음
        # 일단 브라우저인척 이 페이지에 로그인 정보 보냄
        url = 'https://sso.snu.ac.kr/safeidentity/modules/auth_idpwd'
        data = {'si_id': username, 'si_pwd':password, 'si_redirect_address':'https://sso.snu.ac.kr/snu/ssologin_proc.jsp?si_redirect_address=http://etl.snu.ac.kr/'}
        res = session.post(url, headers=login_headers, data=data)
        
        text = res.text

        if text.find('<form method="POST">')==-1:
            return None
        """
        body onload="document.forms[0].action='https://'+window.location.hostname+'/nls3/fcs';document.forms[0].submit();">
            <form method="POST">
                    <input type=hidden name=cmd value="Verify3rdPartyNonce">
                    <input type=hidden name=toa value="1">
                    <input type=hidden name=userid value="v199GZ435MtB68fVF9W0mQ==">
                    <input type=hidden name=nonce value="3RL98DEm50ng8AoxS9EEKo9hFERe3yTRKoik0q3nw1omaVct8PTETe9eXtj0TZh+KBCgdErcYDaY+pc7v1zMmA==">
                    <input type=hidden name=signature value="VXR+Qzs0fNMk00eok0gJp21wC5Nx2F/W7EIYbSU/8/Ft4O/qD3y9W+5C5HOcgHwmxvEkfWDW0D132kVwK4EMq5FI566Tfb4D5lhZ1LolwEc3HI3x2xqIW5xaKflkitd5tDICS9if3Jfq8nQ/wQRRJ9Aot833SrKXgOr1AMNWZHIDhRTetcsRJ2Na7CSH8PsAOZtqr1XSmmRZBw93BMXwqXdA2K1M2pajJLWuNWxNUHtGP2jQcxiaO/2Czn7nZQs3ufrv7DoVuXe65Lt78mrqJG/wUXRY/Zkizxq0w3Vu+vJ6cdgeYxRJUTI6m58qp6bIjxk6gF34NSmwBIztvkV98Q==">
                    <input type=hidden name=certificate value="MIIDrTCCApWgAwIBAgIDAg3uMA0GCSqGSIb3DQEBCwUAMFMxCzAJBgNVBAYTAktSMRAwDgYDVQQKEwdJTklURUNIMREwDwYDVQQLEwhQbHVnaW5DQTEfMB0GA1UEAxMWSU5JVEVDSCBQbHVnaW4gUm9vdCBDQTAeFw0xMzA1MDIwMTExMThaFw0yMzA1MDIwMTExMTdaMDkxCzAJBgNVBAYTAktSMRIwEAYDVQQKEwlJTklURUNIQ0ExFjAUBgNVBAMTDXNzby5zbnUuYWMua3IwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDGS24D9nXWsPtlgbFL3M2GSUN+OuKOrjUMUyGWZ4CnjrEPAxq8ISWzb3zUZfpDWmG45bV6N3196RQ64Vx3WtY5ekA5NjK6iIruifXTCCX9xjYAOGnWWtlE2tesepirt64ZnDUHxkOPF4Nrr31rqnAv6pT/NStAk3WCOAXTeUzbMvy71PDBMfFoUTBD07WcXgzskpN2StDeYhaZ3gcZEbwchpTBeDGjDESxw/JNtIdWpMpUAWLLmEyITC9GnkST4Ffjx7jQ2TpGH3Qz6jPZ4AK52Yv/0HlvrCed6TXeL7iBQ2HArW2M0ysuR2fQEK9n0XJC/j/V2KwS8fhblAG6nnXfAgMBAAGjgaMwgaAwHwYDVR0jBBgwFoAUdZHynOrUueejpV93hNuhGg0Yi6UwHQYDVR0OBBYEFMSPiCzVp/qr1uLuXcjSkP7r8VrJMA4GA1UdDwEB/wQEAwIB/jAMBgNVHRMBAf8EAjAAMEAGA1UdHwQ5MDcwNaAzoDGGL2h0dHA6Ly8xMTguMjE5LjU1LjEzOTo0ODIwMC9DUkwvSU5JVEVDSENBMTMuY3JsMA0GCSqGSIb3DQEBCwUAA4IBAQAExssJPEe/7TMjPnNlCT0nd8Nvbr9tUFO38EgTl9yKQXvCczcX5AvP7YTmXOeiQ6Lc2C4Ea+mFqsFVxt8te4B4rScZ252N2xr1hvyJo8NcTSgr5VTm7s0ZwojxbdE2W9OaG2HuKHbGu2Le/tqaDQ9l41FpNavjlVWg26FU3rpmm5C5a1/Mm0flVfYzUan00KAXFrRXzMMV4NE9RevAYdM0MdGIIDop4Hvd0md/yJPhOY36mLy3NW3onbCLXVSkLDbw14IQ+MScS3cJkd6zVQMXb9C5/G33JIpRa+Pp97/q7HU05CdBWuXB5BK/AU76l9No9y8oeEcEF03Xco/a6PaJ">
            </form>
            </body>
        """
        # 그럼 위처럼 id, pass 도 변환되어 있고 인증 세션값이 포함된 새로운 form을 줌
        # 웹이라면 그대로 redirect되기 때문에 로그인이 되지만, python requests에서는 수동으로 해줘야함.
        # form 에 있는 정보를 data로 변환해서 다시 post
        
        url = 'https://sso.snu.ac.kr/nls3/fcs'
        inputs = re.compile(r'name=(?P<key>\w+)\svalue=\"(?P<value>.*?)\"', re.MULTILINE).finditer(text)
        data = {}
        for input in inputs:
            data[input.group('key')] = input.group('value')
        res = session.post(url, data=data)

        # 자동적으로 쿠키가 설정되어 있고 필요한 값 얻어짐.
        print(f"쿠키값 : {session.cookies['MoodleSessionnewetlcm']}")
        return 'MoodleSessionnewetlcm='+session.cookies['MoodleSessionnewetlcm']

    def get_page_list(url, username, password):
        # expire되서 확인 결과 이 값이 개인을 구분하는 값
        cookie = get_cookie(username, password)
        if cookie:
            headers['Cookie'] = cookie
        else:
            msgbox.showwarning('경고', 'url, 아이디, 비밀번호를 제대로 입력했는지 확인해주세요')
            return
        # 위 로그인 header 사용시 로그인 된것으로 인식함.
        res = requests.get(url, headers=headers)
        root = html.fromstring(res.text)
    
        # 크롤링에 bs 보다 lxml이 모든게 좋음
        tags = root.xpath('//div[@class="activityinstance"]')
        page_list = []
        length_of_tags = len(tags)
        for idx, tag in enumerate(tags):
            a_tag = tag.xpath('a')[0]
            match = re.compile(r"window\.open\(\'(?P<url>.*?)\',").match(a_tag.attrib['onclick'])
            if match:
                entity = {}
                entity['name'] = a_tag.text_content()
                entity['url'] = match.group('url')
                for count in range(1, 10):
                    # 영상 페이지 데이터 가져와서 m3u8 값 추출
                    print(f"{entity['name']} 주소 추출중..")
                    page = requests.get(entity['url'], headers=headers)
                    match_2 = re.compile(r".*?file.*?(?P<url>http.*?playlist\.m3u8)\'}").search(page.text)
                    if match_2:
                        entity['m3u8'] = match_2.group('url')
                        print(entity['m3u8'])
                        break
                    else:
                        print(str(count)+'번째 시도 실패')
                        progress = (idx+1)/length_of_tags*100
                        p_var.set(progress)
                        progress_bar.update()

                page_list.append(entity)
            #프로그레스 바 업데이트
            progress = (idx+1)/length_of_tags*100
            p_var.set(progress)
            progress_bar.update()

        return page_list

    def get_vid_names_url(url, username, password):
        # expire되서 확인 결과 이 값이 개인을 구분하는 값
        cookie = get_cookie(username, password)
        if cookie:
            headers['Cookie'] = cookie
        else:
            msgbox.showwarning('경고', 'url, 아이디, 비밀번호를 제대로 입력했는지 확인해주세요')
            return
        # 위 로그인 header 사용시 로그인 된것으로 인식함.
        res = requests.get(url, headers=headers)
        root = html.fromstring(res.text)
    
        # 크롤링에 bs 보다 lxml이 모든게 좋음
        tags = root.xpath('//div[@class="activityinstance"]')
        page_list = [{'name': 'all', 'url': 'all'}]

        for idx, tag in enumerate(tags):
            a_tag = tag.xpath('a')[0]
            match = re.compile(r"window\.open\(\'(?P<url>.*?)\',").match(a_tag.attrib['onclick'])
            if match:
                entity = {}
                entity['name'] = a_tag.text_content()
                entity['url'] = match.group('url')
                page_list.append(entity)


        return page_list

    def get_address(name, url):
        for count in range(1, 10):
            # 영상 페이지 데이터 가져와서 m3u8 값 추출
            print(f"{name} 주소 추출중..")
            page = requests.get(url, headers=headers)
            match_2 = re.compile(r".*?file.*?(?P<url>http.*?playlist\.m3u8)\'}").search(page.text)
            if match_2:
                m3u8_file = match_2.group('url')
                print(m3u8_file)
                break
            else:
                print(str(count)+'번째 시도 실패')
        return m3u8_file

    def download(save_path, data):
        # name, playlist_url = data
        # command = f'{os.path.join(os.path.dirname(__file__), "ffmpeg.exe")} -y  -i {playlist_url} -c copy "{os.path.join(save_path, name + ".mp4")}"'
        # print(command)

        # process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        # ret = []
        # with process.stdout:
        #     try:
        #         for line in iter(process.stdout.readline, ''):
        #             ret.append(line.strip())
        #             print(line.strip())
        #     except: 
        #         pass
        # process.wait()
        name, playlist_url = data
        print(playlist_url)
        vid_url = re.search(r'.*?mp4\/', playlist_url).group()
        r = requests.get(playlist_url)
        print(r.text)
        print()
        chunklist_url = vid_url+ r.text.split('\n')[3]
        r=requests.get(chunklist_url)
        m3u8_master = m3u8.loads(r.text)
        print(r.text)
        with open(os.path.join(save_path, (name+".ts")),'wb') as f:
            length_of_segments = len(m3u8_master.data['segments'])
            for idx, segment in enumerate(m3u8_master.data['segments']):
                #프로그레스 바 업데이트
                progress_2 = (idx+1)/length_of_segments*100
                p_var_2.set(progress_2)
                progress_bar_2.update()
                r=requests.get(vid_url+segment['uri'])
                f.write(r.content)
                #프로그레스 바 업데이트
                progress_2 = (idx+1)/length_of_segments*100
                p_var_2.set(progress_2)
                progress_bar_2.update()

        os.rename(os.path.join(save_path, name+".ts"), os.path.join(save_path, name +".mp4"))

    def open_help():
        webbrowser.open_new("https://rlawogus0502.github.io/help_doc/snu_etl_help.html")
    root = Tk()
    root.title("etl_video_downloader")  
    root.geometry("640x360") #가로*세로

    #menu
    menu =Menu(root)
    menu_file = Menu(menu, tearoff=0)
    menu_file.add_command(label="Exit", command=root.quit)
    menu.add_cascade(label="Exit", menu=menu_file)
    menu_help = Menu(menu, tearoff=0)
    menu_help.add_command(label="help", command= open_help)
    menu.add_cascade(label="Help", menu= menu_help)
    root.config(menu=menu)

    # 맨 윗줄에 입력받는 frame
    insert_frame = Frame(root)
    insert_frame.pack(side="top", fill="x")
    Label(insert_frame, text="영상들이 있는 url: ", width="0", padx=5, pady=5).pack(side="left")
    url_entry = Entry(insert_frame, width=20)
    url_entry.pack(side='left')
    Label(insert_frame, text="아이디: ", width="0", padx=5, pady=5).pack(side="left")
    username_entry = Entry(insert_frame, width=15)
    username_entry.pack(side='left')
    Label(insert_frame, text="비밀번호: ", width="0", padx=5, pady=5).pack(side="left")
    password_entry = Entry(insert_frame, width=15)
    password_entry.pack(side='left')

    
    def show_lectures():
        progress_frame.pack(fill="x")
        progress_bar.pack(fill="x")
        url = url_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        # data = get_page_list(url, username, password)
        page_list = get_vid_names_url(url, username, password)
        lecture_names = [dic['name'] for dic in page_list]
        lecture_dict = {}
        for dic in page_list:
            lecture_dict[dic['name']] = dic['url']
        progress_frame.pack_forget()
        progress_bar.pack_forget()
        # for item in data:
        #     lectures[item['name']] = item['m3u8']

        combobox_frame = Frame(root)
        combobox_frame.pack(fill="x")
        Label(combobox_frame, text="다운받을 강좌", width="0", padx=3, pady=5).pack(side="left")
        combobox_lecture = ttk.Combobox(combobox_frame, height=0, values=lecture_names, state="readonly")
        combobox_lecture.current(0) #0번째 index선택
        combobox_lecture.pack(side="left", padx=2, pady=5)
        combobox_lecture.set(lecture_names[0])
        def ready_for_down():
            key = combobox_lecture.get()
            save_path = txt_dest_path.get()
            if not save_path:
                msgbox.showwarning('경고', '저장 경로를 입력하세요')
                return
            if key == 'all':
                for key in lecture_names:
                    if key=='all':
                        continue
                    
                    key_frame = Frame(root)
                    key_frame.pack(fill="x")
                    progress_frame_2.pack(fill="x")
                    progress_bar_2.pack(fill="x")
                    Label(key_frame, text=f"{key} 다운로드 중: ").pack(side="left")
                    lecture_address = get_address(key, lecture_dict[key])
                    if os.path.exists(f"{key}.mp4") == False and lecture_address!=None:
                        print(f"{key}, {lecture_address}")
                        download(save_path, (key, lecture_address))

                    key_frame.pack_forget()
                    progress_frame_2.pack_forget()
                    progress_bar_2.pack_forget()
            else:
                key_frame = Frame(root)
                key_frame.pack(fill="x")
                progress_frame_2.pack(fill="x")
                progress_bar_2.pack(fill="x")
                Label(key_frame, text=f"{key} 다운로드 중: ").pack(side="left")
                #print(json.dumps(data, indent=4, ensure_ascii=False))
                lecture_address = get_address(key, lecture_dict[key])
                if os.path.exists(f"{key}.mp4") == False and lecture_address!=None:
                    print(f"{key}, {lecture_address}")
                    download(save_path, (key, lecture_address))
                
                key_frame.pack_forget()
                progress_frame_2.pack_forget()
                progress_bar_2.pack_forget()
            msgbox.showinfo('알림', "저장이 완료되었습니다!")

        btn_start_down = Button(combobox_frame, text="다운로드", command=ready_for_down)
        btn_start_down.pack(side="left")

    #저장 경로 입력받기
    def browse_dest_path():
        folder_selected=filedialog.askdirectory()
        if folder_selected==None:
            return
        txt_dest_path.delete(0,END)
        txt_dest_path.insert(0, folder_selected)

    path_frame = LabelFrame(root, text="저장경로")
    path_frame.pack(fill="x", padx=5, pady=5)
    txt_dest_path =Entry(path_frame)
    txt_dest_path.pack(side="left", fill="x", expand=True, ipady=4)
    btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browse_dest_path)
    btn_dest_path.pack(side="right")

    ready_down_btn = Button(root, text="영상 이름 불러오기", width=20, command=show_lectures)
    ready_down_btn.pack()
    
    #진행상황
    p_var = DoubleVar()
    progress_frame = LabelFrame(root, text="영상 이름 추출 중")
    progress_bar = ttk.Progressbar(progress_frame, maximum=100, variable=p_var)

    p_var_2 = DoubleVar()
    progress_frame_2 = LabelFrame(root, text= "영상 다운로드 중")
    progress_bar_2 = ttk.Progressbar(progress_frame_2, maximum=100, variable=p_var_2)
    root.mainloop()

if __name__ == '__main__':
    main()