# Contributing to Smart Drone Detection System

First off, thank you for considering contributing to the Smart Drone Detection System! It's people like you that make open-source software such a great community.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](../../issues) page to see if someone else in the community has already created a ticket. If not, go ahead and make one!

## Fork & create a branch

If this is something you think you can fix, then fork the repository and create a branch with a descriptive name.

```bash
git checkout -b fix/webcam-crash
# or
git checkout -b feature/thermal-camera-support
```

## Get the test suite running

Make sure your environment is set up.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the application locally to ensure your baseline is working before making changes:

```bash
streamlit run streamlit_app.py
```

## Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first.

## Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with the main repository.

```bash
git remote add upstream https://github.com/Krishna270704/smart-drone-detection-system.git
git checkout main
git pull upstream main
```

Then update your feature branch from your local copy of main, and push it!

```bash
git checkout feature/your-feature
git rebase main
git push --set-upstream origin feature/your-feature
```

Finally, go to GitHub and make a Pull Request! Please provide a detailed description of what you changed.
