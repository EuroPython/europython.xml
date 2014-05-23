Generate brochure (talks)
-------------------------

bin/schedulexml2brochure -i session-export-20140518.1800.xml -p pdfreactor -f out.pdf -t brochure_talks.pt -y /path/to/fonts

Generate brochure (speakers)
----------------------------

bin/schedulexml2brochure -i session-export-20140518.1800.xml -p pdfreactor -f out.pdf -t brochure_speakers.pt -z session-export-20140518.1800 -y /path/to/fonts


Templates
---------

-> epxml/templates/

Styles
------

-> epxml/templates/resources/

! Free fonts can be stored within the epxml/templates/resources directory and pushed to Github.
! Non-free fonts must kept separated and configured using the '-y' or '--fontpath' option.

