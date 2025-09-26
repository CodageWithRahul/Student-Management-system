# Base image with OpenJDK and Python
FROM ubuntu:22.04

# Install Java, Python, pip, curl, Tomcat
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk python3 python3-pip curl unzip tomcat9 tomcat9-admin && \
    apt-get clean

# Copy WAR file into Tomcat
COPY captcha/CaptchaService.war /var/lib/tomcat9/webapps/ROOT.war

# Copy Flask app
COPY SMS /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 5000 8080

# Start both services
CMD service tomcat9 start && python3 app.py
