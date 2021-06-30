import os
import requests
from datetime import date
import json

def call_github():

# make the github request
  params = {'state':'open'}
  headers = {'User-Agent':'request','Authorization':'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'}
  resp = requests.get('https://api.github.com/repos/Slackbot-Hackathon/slackbot_hackathon/pulls', params=params, headers=headers)

  if resp.status_code != 200:
      print(resp.status_code)
      print(resp.json())

  result = []

  for pr in resp.json():
      # parse requested reviewers
      requested_reviewers = pr['requested_reviewers']
      reviewer_usernames = []
      for reviewer in requested_reviewers:
          reviewer_usernames.append('<@' + reviewer['login'] + '>')

      # get days open
      created_at = pr['created_at'].split("-")
      d0 = date(int(created_at[0]), int(created_at[1]), int(created_at[2][:2]))
      days_open = date.today() - d0

      # construct output
      title = pr['title']
      url = pr['url']
      story_num = title.split(":")[0]

      all_reviewer_usernames = ", ".join(reviewer_usernames)


      commit = pr['head']['sha']
      params = {'per_page':1}
      resp = requests.get('https://api.github.com/repos/Slackbot-Hackathon/slackbot_hackathon/commits/' + commit + '/check-runs', params)
      check_resp = resp.json()
      # print('\n\n\n')
      # print(resp.json())
      pr_status = check_resp['check_runs'][0]['conclusion']

      # construct json and write to file
      pr_obj = {}
      pr_obj['title'] = title
      pr_obj['url'] = url
      pr_obj['story_num'] = story_num
      pr_obj['reviewer_usernames'] = all_reviewer_usernames
      pr_obj['days_open'] = days_open.days
      pr_obj['status'] = pr_status
      result.append(pr_obj)

  return result




def call_jira():
  # make the github request
  headers = {'Authorization': 'Basic a21hbmF5ZXJAeWFob28uY29tOjI5U21XeFl2d1dzcjJ6YTdMTDFONDE1Qw==', 'Content-Type': 'application/json'}
  resp = requests.get('https://kmanayer.atlassian.net/rest/agile/1.0/board/1/sprint/1/issue', headers=headers)

  if resp.status_code != 200:
     print(resp.status_code)
     print(resp.json())

  data = resp.json()

  result = []

  for story in data['issues']:
    story_obj = {}
    story_obj['project_name'] = story['fields']['project']['name']
    story_obj['project_url'] = story['fields']['project']['self']
    story_obj['sprint_name'] = story['fields']['sprint']['name']
    story_obj['sprint_start_date'] = story['fields']['sprint']['startDate']
    story_obj['sprint_end_date'] = story['fields']['sprint']['endDate'][:10]
    story_obj['story_name'] = story['key']
    story_obj['story_url'] = story['self']
    story_obj['priority_num'] = story['fields']['priority']['id']
    story_obj['status'] = story['fields']['status']['name']
    story_obj['assignee'] = story['fields']['assignee']['displayName'] if story['fields']['assignee'] else None
    story_obj['points'] = story['fields']['customfield_10030']

    result.append(story_obj)
  return result

if __name__ == "__main__":
    github_info = call_github()
    jira_info = call_jira()

    failed_emoji = ':red_circle:'
    success_emoji = ':large_green_circle:'
    pending_emoji = ':large_yellow_circle:'

    output_msg = ""
    for pr in github_info:
        for story in jira_info:
            if pr['story_num'] == story['story_name']:
                emoji = pending_emoji
                if (pr['status'] == 'failure'):
                    emoji = failed_emoji
                elif (pr['status'] == 'success'):
                    emoji = success_emoji
                output = emoji + ' ' + pr['title'] + " (" + pr['url'] + ") is awaiting review by " + pr['reviewer_usernames'] +\
                         " and has been open for " + str(pr['days_open'] + 1) + " day. \nStory points: " + str(story['points']) + \
                         "\nTarget end date: " + story['sprint_end_date'] + "\n\n"
                output_msg += output
                continue



    # print message for testing
    print(output_msg)
