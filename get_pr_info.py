import os
import requests
from datetime import date
import json

if __name__ == "__main__":
# make the github request
  params = {'state':'open'}
  resp = requests.get('https://api.github.com/repos/kmanayer/slackbot_hackathon/pulls', params)

  if resp.status_code != 200:
    raise ApiError('GET prs {}').format(resp.status_code)

  result = []

  for pr in resp.json():
      # parse requested reviewers
      requested_reviewers = pr['requested_reviewers']
      reviewer_usernames = []
      for reviewer in requested_reviewers:
          reviewer_usernames.append(reviewer['login'])

      # get days open
      created_at = pr['created_at'].split("-")
      d0 = date(int(created_at[0]), int(created_at[1]), int(created_at[2][:2]))
      days_open = date.today() - d0

      # construct output
      title = pr['title']
      url = pr['url']
      story_num = title.split(":")[0]
      all_reviewer_usernames = ", ".join(reviewer_usernames)

      # print message for testing
      # output = title + " (" + url + ") is awaiting review by " + all_reviewer_usernames + " and has been open for " + str(days_open.days) + " days"
      # print(output)

      # construct json and write to file
      pr_obj = {}
      pr_obj['title'] = title
      pr_obj['story_num'] = story_num
      pr_obj['reviewer_usernames'] = all_reviewer_usernames
      pr_obj['days_open'] = days_open.days
      result.append(pr_obj)

  with open('github_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)