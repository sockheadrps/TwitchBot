#!/bin/bash
tmux kill-session -t bot_session
tmux kill-session -t obs_session
tmux kill-session -t browser_session


# Start a new tmux session for OBS
tmux new-session -d -s obs_session
tmux new-window -t obs_session

# Run flatpak command in the tmux session for OBS
tmux send-keys -t obs_session 'flatpak run com.obsproject.Studio' C-m


# Split the window in the OBS tmux session
tmux split-window -t obs_session



# Create a new tmux session for the browser
tmux new-session -d -s browser_session

# Run Google Chrome with a specific URL in the new browser session
tmux send-keys -t browser_session 'google-chrome https://dashboard.twitch.tv/u/sockheadrps/stream-manager' C-m


sleep 3


# # Start a new tmux session for the bot
tmux new-session -d -s bot_session
tmux new-window -t bot_session

# Activate venv
tmux send-keys -t bot_session 'cd ..' C-m
tmux send-keys -t bot_session 'source .venv/bin/activate' C-m
sleep 1

# Run the Python script for the bot
tmux send-keys -t bot_session 'cd TwitchBot/TwitchBot/' C-m
tmux send-keys -t bot_session 'python3 __main__.py' C-m

# Split the window horizontally in terminal_and_bot
tmux split-window -h -t bot_session

instructions=$'\nsuper ctrl h to cycle window locations\nsuper shift y/o to size window\nctrl+b, then arrow keys to switch tmux panes'

tmux send-keys -t bot_session:1 "echo -e \"$instructions\"" C-m

# Attach to the main session
tmux attach-session -t bot_session
