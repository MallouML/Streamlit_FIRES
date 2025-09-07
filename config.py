"""

Config file for Streamlit App

"""

from member import Member


TITLE = "Prédiction de la classe des feux aux États-Unis"

TEAM_MEMBERS = [
    Member(name = "Maëlle Filopon", 
           linkedin_url = "https://www.linkedin.com/in/maëlle-filopon", 
           github_url = None),
    Member(name = "Yassine Rogui", 
           linkedin_url = None, 
           github_url = None),
    Member(name = "Lévitique Moussavou Moussirou", 
           linkedin_url=None, 
           github_url=None)]

PROMOTION = "Promotion Data Analyst - Janvier 2025"