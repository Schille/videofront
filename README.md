# Videofront
This repository contains a simple video gallery generator and kiosk-mode presenter script. It allows public visitors of
exhibitions to navigate through a set of videos and play them. In order to easily add new categories and videos the overview
is generated from an available set of videos in a directory structure.

## Generator

Place a web-compatible video file (mp4, webm) under `./videos/<category>/`. Then run `generator.py` which picks
up all video files from that directory and integrates that in a kiosk-compatible HTML-based frontend. The web
app supports the navigation with cursor keys only, i.e. navigate through available categories/videos and start playing them
in a lightbox by pressing the space/return key. During video playback, the cursor keys can be used to +/-10 s in the current video; escape 
key stops the video and returns to the gallery overview.

## Presenter

The `presenter.py` starts a Chrom/Chromium in kiosk-mode which hides all browser-elements (address bar, buttons, bookmarks, etc.).
The generated web frontend is displayed and can be shown full screen.

