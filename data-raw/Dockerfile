

FROM rocker/tidyverse:latest

# Install R packages
RUN install2.r --error \
    docopt \
    fst \
    lubridate \
    magrittr

RUN apt-get update && apt-get -y -qq install less time

VOLUME ["/srv"]

CMD ["/usr/bin/bash"]

