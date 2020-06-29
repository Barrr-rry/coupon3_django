#FROM joyzoursky/python-chromedriver:3.7
FROM previous:latest as previous
ENV ENV dev
COPY ./web /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get install libsqlite3-mod-spatialite
#RUN apt-get -y install binutils libproj-dev gdal-bin
#
#RUN wget https://download.osgeo.org/proj/proj-4.9.1.tar.gz && tar xzf proj-4.9.1.tar.gz && cd proj-4.9.1/nad && cd .. && ./configure && make && make install && cd ..
#RUN wget https://download.osgeo.org/proj/proj-datumgrid-1.7.tar.gz
#RUN tar xzf proj-4.9.1.tar.gz
#RUN tar xzf proj-datumgrid-1.7.tar.gz
#
#RUN wget http://download.osgeo.org/geos/geos-3.7.0.tar.bz2 && tar xjf geos-3.7.0.tar.bz2 && cd geos-3.7.0 && ./configure && make && make install && cd ..
#
#RUN wget http://download.osgeo.org/proj/proj-4.9.1.tar.gz && tar xzf proj-4.9.1.tar.gz && cd proj-4.9.1/nad && cd ../../ && wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz && tar xzf proj-datumgrid-1.5.tar.gz && cd proj-4.9.1 && ./configure && make && make install && cd ..
#
#RUN wget http://download.osgeo.org/gdal/2.4.0/gdal-2.4.0.tar.gz && tar xzf gdal-2.4.0.tar.gz && cd gdal-2.4.0 && ./configure --with-python && make && make install && cd ..

CMD python manage.py runserver 0.0.0.0:3322
#RUN apt-get update && apt-get install -y cron
#RUN service cron start
#RUN python manage.py crontab add