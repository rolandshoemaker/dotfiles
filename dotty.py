#!/usr/bin/python3
#        __      __  __       
#   ____/ /___  / /_/ /___  __
#  / __  / __ \/ __/ __/ / / /
# / /_/ / /_/ / /_/ /_/ /_/ / 
# \__,_/\____/\__/\__/\__, /  
#                    /____/   
#
# licensed under the MIT license <http://opensource.org/licenses/MIT>

import platform

COMMON = {
	".Xdefaults": "~/.Xdefaults",
	".zshrc": "~/.zshrc",
	".nanorc": "~/.nanorc",
	".bin": "~/.bin"
}

MACHINES = [
	{
		"hostname": "san",
		"files": {
			
		}
	},
	{
		"hostname": "niya",
		"files": {
			
		},
		"exclude": [
			".Xdefaults"
		]
	},
	{
		"hostname": "moro",
		"files": {
			".i3": "~/.i3",
			".conkyrc": "~/.conkyrc"
		}
	}
]

