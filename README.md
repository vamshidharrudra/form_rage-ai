# FORMRAGE AI

AI-Powered Workout Form Analysis and Fitness Coaching

FORMRAGE AI is a Streamlit-based computer vision application that analyzes workout videos, tracks human body pose, detects repetitions, evaluates exercise form, and provides AI-powered feedback.

The application combines MediaPipe Pose Landmarker, OpenCV, and Groq Vision AI to provide rep-level workout analysis.

## Live Application

https://formrage-ai-gr2m2z7fyxyv5nrueszpk2.streamlit.app/

## GitHub Repository

https://github.com/vamshidharrudra/form_rage-ai

## Problem Statement

Many people perform exercises without knowing whether their technique is correct.

Common problems include:

- Incorrect posture
- Poor joint alignment
- Insufficient range of motion
- Unstable movement
- Incorrect exercise technique
- Lack of personalized feedback

FORMRAGE AI addresses this problem by analyzing workout videos and converting visual movement information into understandable exercise feedback.

## Solution

FORMRAGE AI follows a complete computer vision and AI pipeline:

Video Upload

↓

Video Validation

↓

Frame Extraction

↓

Human Pose Detection

↓

Landmark Tracking

↓

Movement Signal Calculation

↓

Repetition Detection

↓

Exact Repetition Frame Extraction

↓

AI Vision Analysis

↓

Form Scoring

↓

Personalized Feedback

↓

Workout Report

↓

Progress Tracking

## Key Features

### AI Workout Analysis

Upload a workout video and receive an automated analysis of exercise form.

### Continuous Pose Tracking

The application processes representative and movement frames using MediaPipe Pose Landmarker to track body landmarks throughout the workout.

### Repetition Detection

Movement signals calculated from pose landmarks are used to identify completed exercise repetitions.

### Rep-Level Analysis

Instead of analyzing only the complete video, FORMRAGE AI extracts specific repetition frames for detailed AI analysis.

### Form Scoring

Each analyzed repetition can be evaluated using form-related dimensions such as:

- Posture
- Alignment
- Range of motion
- Stability
- Technique

### AI Feedback

The system explains:

- What was performed correctly
- What mistakes were detected
- Why the score was given
- How the user can improve

### Multiple Feedback Modes

FORMRAGE AI provides different feedback experiences:

- Coach
- Teach
- Roast

Coach mode provides supportive professional feedback.

Teach mode focuses on explaining the exercise and technique.

Roast mode provides humorous technique-focused feedback while remaining respectful.

### Exercise Guide

Users can view exercise-specific guidance before performing an exercise.

### Workout Reports

The application generates structured workout analysis and feedback.

### Progress Tracking

Previous workout results can be used to monitor performance over time.

## Supported Exercises

The application currently supports exercises including:

- Squat
- Push-up
- Lunge
- Bicep Curl
- Shoulder Press
- Lateral Raise
- Front Raise
- Sit-up / Crunch
- Jumping Jack

## Technology Stack

### Frontend

- Streamlit

### Computer Vision

- OpenCV
- MediaPipe Pose Landmarker

### Artificial Intelligence

- Groq API
- Vision-capable AI model

### Programming Language

- Python

### Data Processing

- NumPy
- Pandas

### Version Control

- Git
- GitHub

### Deployment

- Streamlit Community Cloud

## AI Architecture

The AI analysis pipeline is divided into several stages.

### Stage 1: Input Validation

The uploaded image or video is validated for quality, format, duration, and suitability.

### Stage 2: Pose Estimation

MediaPipe Pose Landmarker identifies body landmarks from workout frames.

### Stage 3: Movement Analysis

Joint angles and movement signals are calculated from the detected landmarks.

### Stage 4: Repetition Detection

Movement signals are analyzed to identify complete repetitions.

### Stage 5: Exact Rep Extraction

Frames corresponding to individual repetitions are selected for detailed analysis.

### Stage 6: AI Vision Analysis

Groq Vision analyzes the selected frames according to the selected exercise and feedback mode.

### Stage 7: Scoring

The detected form is evaluated using multiple form dimensions and converted into an overall score.

### Stage 8: Feedback Generation

The system generates strengths, mistakes, recommendations, and the main issue requiring improvement.

## Project Structure

```text
FORMRAGE AI
│
├── app.py
├── requirements.txt
├── packages.txt
├── README.md
│
├── assets
│   └── exercises
│
├── core
│   ├── groq_engine.py
│   ├── movement_engine.py
│   ├── prompt_engine.py
│   ├── scoring_engine.py
│   ├── session_manager.py
│   └── validation.py
│
├── data
│   └── exercises.json
│
├── models
│   └── pose_landmarker_full.task
│
├── pages
│   ├── ai_coach.py
│   ├── analyze.py
│   ├── dashboard.py
│   ├── exercise_guide.py
│   ├── progress.py
│   ├── rep_analysis.py
│   └── reports.py
│
└── utils
    ├── image_utils.py
    ├── pose_utils.py
    ├── rep_detector.py
    ├── theme.py
    ├── video_utils.py
    └── visualization.py
