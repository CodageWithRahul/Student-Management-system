# Base image with OpenJDK and Python
FROM ubuntu:22.04

# Install Java, Python, pip, curl
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk python3 python3-pip curl unzip && \
    apt-get clean

# Install Tomcat
RUN curl -O https://downloads.apache.org/tomcat/tomcat-9/v9.0.73/bin/apache-tomcat-9.0.73.tar.gz && \
    tar xvf apache-tomcat-9.0.73.tar.gz && \
    mv apache-tomcat-9.0.73 /opt/tomcat && \
    rm apache-tomcat-9.0.73.tar.gz

# Copy WAR file into Tomcat
COPY captcha/CaptchaService.war /opt/tomcat/webapps/ROOT.war

# Copy Flask app
COPY SMS /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Expose ports
EXPOSE 5000 8080

# Start both services
CMD /opt/tomcat/bin/catalina.sh run & python3 app.py
