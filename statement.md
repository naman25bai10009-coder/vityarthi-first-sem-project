# Student Health & Habit Tracker

## Problem Statement
Engineering students often compromise on sleep and hydration to meet academic deadlines, leading to weakened immunity. The recent rise in Jaundice cases on our campus highlighted how neglecting basic habits can make students vulnerable to infections. This project addresses the lack of self-awareness by providing a simple tool to quantify and monitor daily health habits.

## Scope of the Project
The project is a lightweight, CLI-based application designed for personal use on a local machine.
* **In Scope:** Tracking Sleep, Water, Exercise, and Screen Time; calculating a daily "Health Score"; and storing data permanently in a CSV file.
* **Out of Scope:** Medical diagnosis, cloud syncing, or complex graphical interfaces (GUI).

## Target Users
* **University Students:** Especially hostellers who manage their own daily schedules and diet.
* **Developers/Coders:** Individuals who spend long hours in front of screens and often forget to drink water or move.

## High-level Features
* **Daily Logging:** Quick entry of critical health metrics (Sleep hours, Water glasses, etc.).
* **Smart Scoring:** Auto-calculates a Health Score (0-100) based on weighted logic.
* **Data Persistence:** Automatically saves all records to a local `csv` file so no data is lost.
* **History Review:** Allows users to view a summary of their last 7 days to track consistency.
