from bs4 import BeautifulSoup
import pandas as pd
import time

start_time = time.time()

#target_tag = ['title','titleEng', 'directorNm', 'directorEnNm', 'actorNm', 'actorEnNm']

for year in range(1990, 2022+1):
    
    check = True
    cnt = 0
    while check:
        cnt += 1
        if cnt >= 3: # 3회 이상 읽게 되면 그만두세요.
            break
        # 영화 xml 읽어서 BeautifulSoup에 넣기. (parser는 xml)
        
        with open (f"./movie_xml/{year}'s_movie.xml", "rb") as mx:
            movie_soup = BeautifulSoup(mx, 'xml')
        
        print(f"{year}'s_movie.xml을 읽습니다.")
             
        # 종종 xml 읽는 과정에서 데이터 누락이 있을 수 있으므로 확인을 위해서
        tot_cnt = int(movie_soup.find('TotalCount').text)
        rows = movie_soup.find_all('Row')
        if tot_cnt != len(rows):
            pass
        
        else:
            movie_dict = dict()
            
            title_box = list()
            title_en_box = list()
            director_ko_box = list()
            director_en_box = list()
            actor_box = list()
            actor_ko_box = list()
            actor_en_box = list()
            
            
            for row in rows:
              
                                
                title = row.find('title').text.strip()
                title_box.append(title)
                
                title_en = row.find('titleEng').text.strip()
                title_en_box.append(title_en)
                
                director_ko = row.find('directorNm').text.strip()
                director_ko_box.append(director_ko)
                
                director_en = row.find('directorEnNm').text.strip()
                director_en_box.append(director_en)
                
                actor_container = list()
                actor_ko_container = list()
                actor_en_container = list()
                
                for actor in row.find_all('actor'):
                    actor_ko = actor.find('actorNm').text.strip()
                    actor_en = actor.find('actorEnNm').text.strip()
                    actor_container.append((actor_ko, actor_en))
                    actor_ko_container.append(actor_ko)
                    actor_en_container.append(actor_en)
                
                actor_box.append(actor_container)
                actor_ko_box.append(actor_ko_container)
                actor_en_box.append(actor_en_container)
                
                
            movie_dict['title'] = title_box
            movie_dict['title_en'] = title_en_box
            movie_dict['director_ko'] = director_ko_box
            movie_dict['director_en'] = director_en_box
            movie_dict['actor'] = actor_box
            movie_dict['actor_ko'] = actor_ko_box
            movie_dict['actor_en'] = actor_en_box
                
            pd.DataFrame(movie_dict).to_csv(f"./movie_data/{year}'s_data.csv", index = None)
            
            check = False # 중요.
            
print(f'소요 시간 : {time.time() - start_time}s')