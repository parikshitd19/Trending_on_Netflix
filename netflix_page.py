from config import countries,global_lists_url_additions,date_str_format, base_url, country_lists_url_additions
from helper_functions import  get_date_obj,is_date_valid_to_query,construct_url,get_the_week,get_media_type_geo
from bsoup import BSoup
import json
import datetime

class NetflixPage:
    def __init__(self,geography = 'Global',media_type = '',when = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d")):
        self.geography = self.__verify_geography(geography)
        self.media_type = self.__verify_media_type(media_type)
        self.when = self.__verify_date(when)
        
        self.page_bsoup_obj = BSoup(construct_url(base_url,self.geography,self.media_type,self.when))
        
        self.table_headings = self.__extract_table_heading(self.page_bsoup_obj.get_soup_obj())
        self.table_contents = self.__extract_table_content(self.page_bsoup_obj.get_soup_obj())

        self.start_date, self.end_date = get_the_week(self.page_bsoup_obj.get_soup_obj())
    
    def __str__(self):
        return f"Querying Netflix for Top 10 at {self.geography} \
            for {get_media_type_geo(self.geography,self.media_type)} for the week\
            {self.start_date}-{self.end_date}"
    
    def __verify_geography(self,geography: str)->str:
        if  geography != 'Global' and geography not in countries.keys() and geography not in countries.values():
            raise Exception("Invalid Country Name")
        return countries.get(geography,geography)
    
    def __verify_media_type(self,media_type: str)->str:
         if media_type not in global_lists_url_additions.values() and media_type not in country_lists_url_additions.values():
             raise Exception("Invalid Media Type")
         return media_type
    
    def __verify_date(self,when: str)->str:

        date_time_obj = get_date_obj(when, date_str_format)

        if not is_date_valid_to_query(date_time_obj):
            raise Exception("Invalid date")

        return when
    
    def __extract_table_heading(self,soup_obj):
        """
        Extract the headings of the table being displayed on the webpage
        """
        table_rows = soup_obj.find('table').find('tr')
        
        table_headings = [ele.text for ele in table_rows.find_all('th')]
        table_headings[1] = 'Title'
        table_headings.insert(2,'Weeks in Top 10')
        
        return table_headings
    
    def __extract_table_content(self,soup_obj):
        """
        Extract the content of the table being displayed on the webpage 
        """
        table_rows = soup_obj.find('table').find_all('tr')
        table_rows.pop(0)
        rows = []
        for row in table_rows:
            columns = row.find_all('td')
            
            ranking_title_column = columns.pop(0)
            rank = ranking_title_column.find('span').text
            title = ranking_title_column.find('button').text
            
            values = [int(rank)]+[title]+[ele.text for ele in columns]

            values[2] = int(values[2])
            
            if len(values)>3:
                if values[3] != "":
                    values[3] = int(values[3].replace(',',''))
                else:
                    values[3] = None
                
                values[5] = int(values[5].replace(',',''))
                
                if values[4] != "":
                    values[4] = round(int(values[4].split(':')[0])+int(values[4].split(':')[1])/60,2)
                else:
                    values[4] = None
            
            rows.append(values)
        
        return rows

    def get_json_obj(self):
        """
        Create & return a JSON Object
        """
        obj = self.get_dict_obj()

        return json.dumps(obj,default=str)
    
    def get_dict_obj(self):
        """
        Get the Dict format the Data
        """
        obj = {
            'geography':self.geography,
            'media_type':get_media_type_geo(self.geography,self.media_type),
            'search_date':self.when,
            'list_start_date':self.start_date,
            'list_end_date':self.end_date,
            'list':[
                {
                self.table_headings[j] : self.table_contents[i][j] for j in range(len(self.table_headings))
            } for i in range(len(self.table_contents))
            ]
        }

        return obj
                
        