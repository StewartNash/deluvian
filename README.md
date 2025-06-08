## Introduction

This is a Python program intended to manage torrents and eventually interface with Deluge. I wrote this program to manage torrents across Windows and Linux with an external drive. Torrents were downloaded in Windows with one client, but the torrent list could not be easily reconstructed in Deluge in Ubuntu.

## Description

Each time the application is opened a session is loaded or created. An old session can be opened or a new session created. The session contains the search history. Each time a search is run, the application finds all torrents in the specified directories, all files in the specified directories and then attempts to correlate the files with the torrents.

### GUI Layout

The GUI is laid out into three panels. The left panel contains a list of found torrents. The center panel contains information on the currently selected torrent. The right panel contains the files that are associated with that torrent.

#### Left Panel

The left panel has a list of torrents at the bottom. Above this is a bar which allows going backward or forward a page and also displays the current page and total number of pages. Above this is a bar which allows one to specify a specific page to go to.

#### Center Panel

#### Right Panel

#### Options Menu

The options menu, which can be selected from the menu bar has numerous settings. Some of these include:
- Number of displayed torrents per page


### Application Functionality

## Todo

- Torrent sharing management
  - Share rare torrents
  - Do not share popular torrents

## Future

- Website interface
  - Priority task: will save time!
- Automatically create and upload torrent
- Streaming platform integration
