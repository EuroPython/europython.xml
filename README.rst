Installation::

    > git clone https://github.com/EuroPython/europython.xml.git
    > cd europython.xml
    > virtualenv-2.7 .
    > bin/python setup.py develop


Generate brochure (talks)
-------------------------

bin/schedulexml2brochure -i session-export-20140623.2200.xml -p pdfreactor -f out.pdf -t brochure_talks.pt -y /path/to/fonts

Generate brochure (speakers)
----------------------------

bin/schedulexml2brochure -i session-export-20140623.2200.xml -p pdfreactor -f out.pdf -t brochure_speakers.pt -z session-export-20140623.2200 -y /path/to/fonts


Templates
---------

-> epxml/templates/

Styles
------

-> epxml/templates/resources/

! Free fonts can be stored within the epxml/templates/resources directory and pushed to Github.
! Non-free fonts must kept separated and configured using the '-y' or '--fontpath' option.


Remote conversion
-----------------
If ``PDFreactor`` is not installed locally then use ``-p remote-pdfreactor`` instead of ``-p pdfreactor``.
In this case you need to set the following environment variables::

    export PP_SERVER_URL=<ask info@zopyx.com>
    export PP_AUTHORIZATION_TOKEN=<ask info@zopyx.com>


