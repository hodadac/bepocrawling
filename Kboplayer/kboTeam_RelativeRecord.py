import requests
from bs4 import BeautifulSoup
import pymysql

# sql 삽입 전 저장할 list
kbo_TeamRelativeRecord = []

try:
    url = "https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"summary": "팀간승패표"})

    # 테이블의 각 행을 반복하여 데이터 추출
    for tr in table.find("tbody").find_all("tr"):
        td_elements = tr.find_all("td")
        td_elements_data = {
            "team_Name": td_elements[0].text.strip(),
            "team_Vs1st": td_elements[1].text.strip(),
            "team_Vs2nd": td_elements[2].text.strip(),
            "team_Vs3rd": td_elements[3].text.strip(),
            "team_Vs4th": td_elements[4].text.strip(),
            "team_Vs5th": td_elements[5].text.strip(),
            "team_Vs6th": td_elements[6].text.strip(),
            "team_Vs7th": td_elements[7].text.strip(),
            "team_Vs8th": td_elements[8].text.strip(),
            "team_Vs9th": td_elements[9].text.strip(),
            "team_Vs10th": td_elements[10].text.strip(),
            "team_Total": td_elements[11].text.strip()
        }
        kbo_TeamRelativeRecord.append(td_elements_data)

    db_config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "1234",
        "database": "sportinfo"
    }

    # MySQL 데이터베이스 연결 설정
    # db_config = {
    #     "host": "localhost",
    #     "port": 3306,  # 포트 번호를 별도로 지정
    #     "user": "root",
    #     "password": "1234",
    #     "database": "lee"
    # }

    # MySQL 데이터베이스에 연결
    connection = pymysql.Connect(**db_config)
    cursor = connection.cursor()

    # kbo_TeamRelativeRecord 테이블 생성
    # 승패무 표시 어떻게 할지 고민
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS kbo_TeamRelativeRecord(
        team_Id BIGINT AUTO_INCREMENT PRIMARY KEY,
        team_Name VARCHAR(255),
        team_Vs1st_WLD VARCHAR(255),
        team_Vs2nd_WLD VARCHAR(255), 
        team_Vs3rd_WLD VARCHAR(255),
        team_Vs4th_WLD VARCHAR(255),
        team_Vs5th_WLD VARCHAR(255),
        team_Vs6th_WLD VARCHAR(255),
        team_Vs7th_WLD VARCHAR(255),
        team_Vs8th_WLD VARCHAR(255),
        team_Vs9th_WLD VARCHAR(255),
        team_Vs10th_WLD VARCHAR(255),
	    team_Total_WLD VARCHAR(255)
    );
    """
    cursor.execute(create_table_sql)
    connection.commit()

    # 데이터를 MySQL 테이블에 삽입
    for kbo_team in kbo_TeamRelativeRecord:
        insert_query = """
        INSERT INTO kbo_TeamRelativeRecord (
            team_Name, team_Vs1st_WLD, team_Vs2nd_WLD, team_Vs3rd_WLD, team_Vs4th_WLD, team_Vs5th_WLD,
            team_Vs6th_WLD, team_Vs7th_WLD, team_Vs8th_WLD, team_Vs9th_WLD, team_Vs10th_WLD, team_Total_WLD
        ) 
        VALUES (%s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        """
        val =(
            kbo_team["team_Name"],
            kbo_team["team_Vs1st"],
            kbo_team["team_Vs2nd"],
            kbo_team["team_Vs3rd"],
            kbo_team["team_Vs4th"],
            kbo_team["team_Vs5th"],
            kbo_team["team_Vs6th"],
            kbo_team["team_Vs7th"],
            kbo_team["team_Vs8th"],
            kbo_team["team_Vs9th"],
            kbo_team["team_Vs10th"],
            kbo_team["team_Total"],
        )
        cursor.execute(insert_query, val)

    # 변경 내용을 커밋
    connection.commit()

    # 연결 종료
    cursor.close()
    connection.close()

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP 오류 발생: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"요청 오류 발생: {req_err}")
except Exception as e:
    print(f"오류 발생: {e}")