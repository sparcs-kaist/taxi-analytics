FROM mongo:4.4

# Install gzip
RUN apt-get -qq update; \
    apt-get -qq install gzip

# Copy repo
WORKDIR /home
COPY . .

# RUN mongod & \
#     mongorestore --gzip --db taxi --archive=20230514T190001.dump.gz & \
#     mongod --shutdown

# Start mongo service
EXPOSE 27017
CMD ["sh", "-cs", "mongod --bind_ip_all & mongorestore --gzip --db taxi --archive=20230514T190001.dump.gz & tail -f /dev/null"]
# CMD ["mongod"]
