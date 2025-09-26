# Use official Tomcat as base
FROM tomcat:9.0.73-jdk17

# Install Python and pip
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Copy Captcha WAR
COPY captcha/CaptchaService.war /usr/local/tomcat/webapps/ROOT.war

# Copy Flask SMS app
COPY SMS/ /app
WORKDIR /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 5000 8080

# Start both services
CMD ["/bin/bash", "-c", "/usr/local/tomcat/bin/catalina.sh run & python3 /app/app.py"]
