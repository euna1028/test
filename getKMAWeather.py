# -*- coding:utf-8 -*- 
from http.client import HTTPSConnection
from xml.etree.ElementTree import fromstring
from cx_Oracle import connect
# 기상청 오늘 날씨만 나오게 하기 day 0
# 빅데이터/인공지능 1단계 : 분석용 데이터 구축 
# 이걸 db에 저장하기 매일 아침...실행하면 됨 
# 어느...db에 저장을?....이건 정형 데이터니깐 오라클에 저장
# 실행하면 기상청에서 오늘 예보만 받아서 내 db에 저장하는 프로그램 
# 오라클에 날짜 시간 기온 날씨 테이블 만들어서 나오게 하기
huc = HTTPSConnection('www.kma.go.kr') #-> import 빨간줄 무시하기 
huc.request('GET', '/wid/queryDFSRSS.jsp?zone=1150055000') #폴더/파일명?파라미터

resBody = huc.getresponse().read()
#kmaData = fromstring(resBody)
# 제이쿼리에서 $(kmadata).find("data")
#->파이썬에서 데이터들을 찾을 때는 getiterator
weathers = fromstring(resBody).getiterator('data') 

con = connect('sdedu/sdedu@sdgn-djvemfu.tplinkdns.com:19195/xe')   
cur = con.cursor() #pstmt : 자동 commit -> 1회용이었지만 
# cur : 수동 commit -> 여러번 사용 가능이라서 반복문 속에 안들어가도 됨 

for w in weathers:
    if w.find('day').text == '1':
        break
    sql = "insert into kma_weather_euna values(sysdate, "
    sql += "%s, "  % w.find("hour").text
    sql += "%s, " % w.find("temp").text 
    sql += "'%s')" % w.find("wfKor").text
    cur.execute(sql) # -> 실행 

con.commit() #-> 이거 써야 반영됨
cur.close()
con.close()
huc.close()
