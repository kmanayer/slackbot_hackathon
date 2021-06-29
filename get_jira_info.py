import os
import requests
from datetime import date
import json

if __name__ == "__main__":
  # make the github request
  headers = {'Authorization': 'Basic a21hbmF5ZXJAeWFob28uY29tOjI5U21XeFl2d1dzcjJ6YTdMTDFONDE1Qw==', 'Content-Type': 'application/json'}
  resp = requests.get('https://kmanayer.atlassian.net/rest/agile/1.0/board/1/sprint/1/issue', headers=headers)

  if resp.status_code != 200:
    raise ApiError('GET prs {}').format(resp.status_code)

  data = resp.json()
  
  result = []

  for story in data['issues']:
    story_obj = {}
    story_obj['project_name'] = story['fields']['project']['name']
    story_obj['project_url'] = story['fields']['project']['self']
    story_obj['sprint_name'] = story['fields']['sprint']['name']
    story_obj['sprint_start_date'] = story['fields']['sprint']['startDate']
    story_obj['sprint_end_date'] = story['fields']['sprint']['endDate']
    story_obj['story_name'] = story['fields']['summary']
    story_obj['story_url'] = story['self']
    story_obj['priority_num'] = story['fields']['priority']['id']
    story_obj['status'] = story['fields']['status']['name']
    story_obj['assignee'] = story['fields']['assignee']['displayName'] if story['fields']['assignee'] else None
    story_obj['points'] = story['fields']['customfield_10030']
    result.append(story_obj)

  print(json.dumps(result, indent=2))


  with open('jira_data.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)