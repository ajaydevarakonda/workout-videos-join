#!/usr/bin/env python
from __future__ import print_function
import os
import operator
import subprocess
import calendar
import re


def get_majority_bow(video_files):
  bow_count = {}

  for name in video_files:
    name = name.split('_')

    if len(name) != 3:
      print("Video file names should be of format VID_<date>_time.mp4")
      print("Not like", name[0])
      print("Skipping...")
      print()
      continue

    bow_name = '_'.join(name[:2])

    if bow_name in bow_count:
      bow_count[bow_name] += 1
    else:
      bow_count[bow_name] = 1

  return max(bow_count.items(), key=operator.itemgetter(1))[0]



def get_filenames():
  files = os.listdir('.')
  video_files = []

  for name in files:
    if '.mp4' in name:
      video_files.append(name)

  majority_bow = get_majority_bow(video_files)
  files_with_majority_bow = []

  for name in video_files:
    if majority_bow in name:
      files_with_majority_bow.append(name)

  return files_with_majority_bow


def write_filenames_to_file(filenames):
  inputs_file = open("inputs.txt", 'w')

  for name in filenames:
    inputs_file.write("file '" + name + "'\n")


def date_to_videotitle(date):
  year = date[:4]
  month = date[4:6]
  day = date[6:8]
  return '{} {} {}th -- Exercise session'.format(year, calendar.month_name[int(month)], day)

###################################### main #################################3
filenames = get_filenames()
filenames.sort(key=lambda f: int(re.sub('\D', '', f)))
print(filenames)
write_filenames_to_file(filenames)
majority_bow = get_majority_bow(filenames)
date = majority_bow.split('_')[1]
video_title = date_to_videotitle(date) + '.mp4'
subprocess.run(['ffmpeg', '-f', 'concat', '-i', 'inputs.txt', '-vcodec', 'copy', '-acodec', 'copy', video_title])
