# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="mh"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
DISABLE_UNTRACKED_FILES_DIRTY="true"

plugins=(git)

# User configuration

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
# export MANPATH="/usr/local/man:$MANPATH"

source $ZSH/oh-my-zsh.sh

# You may need to manually set your language environment
export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='nano'
  export VISUAL='nano'
else
  export EDITOR='nano'
  export VISUAL='nano'
fi

# added by travis gem
[ -f /home/roland/.travis/travis.sh ] && source /home/roland/.travis/travis.sh

#################
# rando helpers #
#################
host=`uname -s`

################
# bettr prompt #
################
PROMPT='[%{$fg[$NCOLOR]%}%B%n%b%{$reset_color%}@%{$fg[white]%}%m%{$reset_color%}:%{$fg[red]%}%30<...<%~%<<%{$reset_color%}]%(!.#.$) '

###############
# theca stuff #
###############
if [[ "$host" == "Linux" ]]; then
	export THECA_PROFILE_FOLDER=/home/roland/Dropbox/.theca
elif [[ "$host" == "Darwin" ]]; then
	export THECA_PROFILE_FOLDER=/Users/roland/Dropbox/.theca
fi

###########
# aliases #
###########
alias p3=python3
alias ..='cd ..'
alias update='sudo apt-get update && sudo apt-get upgrade'
alias ls='ls -al'