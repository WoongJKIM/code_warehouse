
> 기존에 인터넷에서 찾아서 파이썬 서버 세팅할 경우 ipython으로 notebook을 접속하는 방식으로 최근 버젼(2016-06-13)은 지원하지 않아, 잊어버리기 전에 세팅 방법을 남겨놓음
> -by 개리롱-

### 1.AWS 세팅
* AWS에서 포트 세팅시 기존에 dev-default 세팅과 함께 포트 8888를 추가해야 한다<-이유:notebook 인터프리터가 기본으로 포트 8888이 설정되있기 때문에 접속 포트를 다른거로 바꿀 경우 맘대로 하셔도 됩니다.

### 2.아나콘다 다운로드/설치/환경설정
1. 사이트에서 리눅스 OS 용 다운로드 경로를 복사해 아나콘다 다운로드를 받는다
 * `$wget http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh`
 * [아나콘다 다운로드 사이트](https://www.continuum.io/downloads)
1. 설치 파일을 실행
 * `$bash Anaconda3-4.0.0-Linux-x86_64.sh`
1. .bashrc 파일에 환경변수 설정을 기존에 python 2.7버젼에서 anaconda의 파이썬 버젼으로 변경
 * `$which python`
 * /user/bin/python으로 기존에 python으로 설정되어 있음
 * `$vi .bashrc`
 * `export PATH=/.../anaconda/bin:$PATH`
 * .bashrc 파일에 $PATH를 추가
 * `$source .bashrc`
 * `$which python`
 * /.../anaconda/bin/python으로 변경된 것을 확인할 수 있음

### 3.jupyter 원격서버 설정
1. notebook server 연결 정보 생성
 * `$jupyter notebook --generate-config`
 * .jupyter 경로 안에 jupyter_notebook_config.py가 생성된 것으로 볼 수 있음
2. 비밀번호 생성
 * `$ipython`
 * `from notebook.auth import passwd`
 * `passwd()`
 * 비밀번호를 입력하면 결과물로 'sha1:dsdf...'로 긴 문자가 나옴. 문서에다가 복사 붙여넣기 함(나중에 설정시 필요로 함)
3. 인증성 생성
 * 패스워드가 암호화 되서 보내지기 때문에 인증서가 필요
 * `/home/user/` 경로에서 certificates 폴더를 생성 
 * `$mkdir certificates`
 * certificates 폴더 내에서 OpenSSL을 사용해 인증서를 생성
 * `openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem`
4. 연결 정보 등록
 * jupyter_notebook_config.py 파일 안에 내용 추가
 * `vi .jupyter/jupyter_notebook_config.py`
 * `c= get_config()`<br>
   `c.IPKernelApp.pylab='inline'`<br>
   `c.NotebookApp.certfile=u'/인증서_경로/mycert.pem'`<br>
   `#open ssl로 만든 pem 파일 경로`<br>
   `c.NotebookApp.password =u'sha1:....'`<br>
   `#ssl로 변환된 비밀 번호`
   `c.NotebookApp.ip='*'`<br>
   `#모든IP 접속 허용`<br>
   `#c.NotebookApp.open_brower=False`<br>
   `#로컬에서 notebook 앱을 브라우져로 실행시킬건지`<br>
   `c.NotebookApp.port_retries = 8888'`<br>
   `#포트 번호 설정`<br>
5. 실행
 * `$nohup jupyter lab --ip=* --no-browser --port 5051 > jupyter.log &`
 * 실행 시 꺼지지 않고, 작동 로그가 jupyter.log 파일에 남음

### 4. 필수 설치 library
 + 개발 모드
   - `apt-get install python-pip`
    - `sudo apt-get install python3-dev`
    - `sudo apt-get install python-dev libmysqlclient-dev`
 + pymongo
   - `pip install pymongo`
 + Mysql
   - `pip install mysqlclient`
 + matplotlib
   - `pip install matplotlib`
   - `sudo apt-get install libsm6 libxrender1 libfontconfig1`
 + Seaborn<-그래프 시각화 라이브러리
   - `pip install seaborn`
 + geopandas<-지도 좌표 정보 라이브러리, 순서 중요
   - pyproj, GDAL, Fiona, Shapely 라이브러리 설치
      * `pip install pyproj`
      * `conda install gdal`
      * `pip install fiona`
      * `pip install shapely`
    - geopandas 라이브러리 설치
        * `pip install geopandas`
 + folium<-지도 시각화 라이브러리
   - `pip install folium`
 + slackweb<-슬랙 애드훅과 연결 시켜주는 라이브러리
   - `pip install slackweb`
 + gspread<-구글 스프레드 연동 라이브러리
   - gspread 라이브러리 설치
     * `pip install gspread`
   - oauth 인증 관련 라이브러리 설치
     * `pip install --upgrade oauth2client`
     * `pip install PyOpenSSL`

### 5. DB 터널링
 + 가비아에 있는 DB의 경우 터널링 필요
   - `ssh -M -S DB명 -fnNT -L 로컬포트:로컬 IP:3306 root@DB IP  -DB포트`

### 6. matplotlib 한글 깨짐
 + 그래프를 출력할 때 한글이 들어가면 깨지는 현상(matplotlib에 기본 글꼴이 한글을 지원 안해 한글 글꼴을 추가 시켜줘야 함)
   - 나눔글꼴 설치(나눔 글꼴 폰트를 받아 설치하고 캐쉬를 재설정하는 순서)
     * `sudo apt-get update`
     * `apt-get install fonts-nanum*`
     * `fc-cache -f -v`
   - matplotlib 내에서 설정(다운 받은 글꼴을 확인해 이름을 설정하고 matplotlib에 설정, 기존에 설정된 글꼴 캐쉬를 삭제
     * `matplotlib.font_manager.get_fontconfig_fonts()`
     * `krfont = {'family' : 'NanumGothic', 'weight' : 'bold', 'size'   : 10}`
     * `matplotlib.rc('font', **krfont)`
     * `rm /home/usr/.cache/matplotlib/cache파일`
   - 한글 글꼴 사용시
     * 한글이 사용될 부분 앞에 이 문구를 선언
     * `mpl.rc('font', family='NanumGothic')`

### 7. folium에서 IFrame 사용시 한글 깨짐
 + folium에서 IFrame을 한글을 사용할 경우 charset-utf-8이란 지정이 없어 한글이 깨지는 경우가 발생
   - 아래 파일 안에 렌더 함수 내에 html 변수 안에 "data:text/html;base64"->"data:text/html;charset=utf-8;base64"
   - `anaconda3/lib/python3.5/site-packages/folium/element.py`
   - `charset=utf-8`이 부분을 추가
   
### 8. 파이썬에서 구글 spread sheet 컨트롤
 + 구글 개발자에서 인증서를 받음
 + gspread 설치
   - `pip install gspread`
 + oauth2client 업데이트
   - `pip install --upgrade oauth2client`
 + PyOpenSSL 설치
   - `pip install PyOpenSSL`
 + 업데이트나 생성하려는 구닥에 사용자 권한에 인증서의 사용자를 추가
