# File Integrity Monitor

A small Python utility to snapshot SHA-256 hashes of files and compare later snapshots to spot additions, changes, and removals.

## Run

`python monitor.py snapshot ./folder` creates or refreshes `integrity.json`. `python monitor.py check ./folder` reports changes without modifying the baseline.

Keep the baseline somewhere attackers cannot alter alongside the monitored files for stronger tamper detection.

## Stack

Python, pathlib, SHA-256, JSON
