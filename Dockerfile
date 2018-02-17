FROM continuumio/anaconda

MAINTAINER rohanraja9@gmail.com

# Configure the main working directory. This is the base
# directory used in any further RUN, COPY, and ENTRYPOINT
# commands.
ENV APP_HOME /apps/xlearn2
RUN mkdir -p /$APP_HOME
WORKDIR /$APP_HOME

# Copy the Gemfile as well as the Gemfile.lock and install
# the RubyGems. This is a separate step so the dependencies
# will be cached unless changes to one of those two files
# are made.
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Copy the main application.
COPY . ./

ENV PYTHONPATH $PYTHONPATH:/apps

WORKDIR /$APP_HOME/tests
# CMD py.test -s webserver_test.py
# CMD ["py.test", "-s", "-v", "webserver_test.py"]
CMD py.test -s
