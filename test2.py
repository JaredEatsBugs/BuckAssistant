from assistant import Assistant
from BuckAD.ClassInfoModule import ClassInfoModule
from watson_developer_cloud import DiscoveryV1
import searchEngine
assistant=Assistant()
brain = DiscoveryV1(
    version='2018-01-01',
    username='c7721aaf-1c20-4325-bb11-6cfe0cdb8967',
    password='2UOJ7kgQHbXH',
    url='https://gateway.watsonplatform.net/discovery/api'
)
discovery=ClassInfoModule(brain)
user_input=''
# query=assistant.get_intent_and_entity('who teaches CSE5526',to_string=True)
# queryr=assistant.get_intent_and_entity('who teaches CSE5526',to_string=False)

while user_input!='exit':
    user_input=input('>')
    queryr=assistant.get_intent_and_entity(user_input,to_string=False)
    if ('course_num' in queryr[1]):
        search_parameters = queryr[1].get('course_num')
    elif ('semesters' in queryr[1]):
        search_parameters = queryr[1].get('semesters')
    elif ('sys-number' in queryr[1]):
        search_parameters = queryr[1].get('sys-number')
    elif ('sys-person' in queryr[1]):
        search_parameters = queryr[1].get('sys-person')
    result = getattr(searchEngine, queryr[0][0])(search_parameters)
    # discovery.run_query(query)
    # result = discovery.retrieve_first_doc_text()
    print(result)