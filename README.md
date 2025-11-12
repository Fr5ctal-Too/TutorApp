# Tutor Me

A modern tutoring platform that combines adaptive AI coaching with human tutors to accelerate mastery. Built for individualized learning, measurable progress, and seamless collaboration between students, parents, and educators.

## Key features
- Personalized learning paths generated from initial diagnostics and ongoing performance.
- Hybrid AI + human workflow: AI tutors provide hints, explanations, and practice; human tutors supervise, review, and mentor.

## How Tutor Me differs from a regular tutor app
- Adaptive curriculum that reshapes itself from continuous assessment (not static lesson lists).
- Hybrid model — AI handles immediate reinforcement and practice; humans handle nuance, motivation, and high-level mentorship.
- Explainability: all AI hints include reasoning traces and sources to support learning, not opaque answers.
- Portable progress: standardized, exportable learning records to use across schools or platforms.

## Installation
To install, clone the repo.
Make sure python is installed.

Run
```
pip install uv
```
to install uv.

Then run
```
uv init
uv venv
```

This project requires gemini and huggingface api keys, stored as `GEMINI_KEY` and `HF_KEY` in environment variables.

To run server,
```
uv run server.py
```

To run client,
```
uv run client.py
```

Default host is `localhost` and port is `5555`. You can edit in config.py.
