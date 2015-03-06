# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load.
ZSH_THEME="mh"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
DISABLE_UNTRACKED_FILES_DIRTY="true"

plugins=(git)

# User configuration

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"

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
export THECA_PROFILE_FOLDER=$HOME/Dropbox/.theca

###########
# aliases #
###########

if [[ "$host" = "Linux" ]]; then
	alias update='sudo apt-get update && sudo apt-get upgrade'
	alias apt-get='sudo apt-get'
	alias ls='ls --color=auto'
	alias ll='ls -al --color=auto'
	alias l.='ls -d .* --color=auto'
	alias sz='ls -l --color=auto | sort -n +3 | tail -10'
	alias -g L="| less"
	alias rm='rm --preserve-root'
	alias chown='chown --preserve-root'
	alias chmod='chmod --preserve-root'
	alias chgrp='chgrp --preserve-root'
fi

alias p=python3
alias ..='cd ..'
alias j='jobs -l'
alias now='date +%T'
alias ping='ping -c 5'
alias fuck='sudo $( history -p \!\!)'
alias s=sudo
alias sudo='sudo '
alias su='sudo -i'
alias reboot='sudo /sbin/reboot'
alias shutdown='sudo /sbin/shutdown'
alias wget='wget -c'
alias df='df -H'

############
# keybinds #
############
sudo-accept-line() {
    if [ -n "${BUFFER## *}" ]; then
        BUFFER="sudo ${BUFFER##sudo }"
        zle end-of-line        
        zle accept-line
    fi
}

zle -N sudo-accept-line
bindkey "^O" sudo-accept-line

#############
# git setup #
#############
if [[ ! -n $( git config --global user.name ) ]]; then
	git config --global user.name "Roland Shoemaker"
fi
if [[ ! -n $( git config --global user.email ) ]]; then
	git config --global user.email rolandshoemaker@gmail.com
fi
if [[ ! -n $( git config --global push.default ) ]]; then
	git config --global push.default simple
fi
