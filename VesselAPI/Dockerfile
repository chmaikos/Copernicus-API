# # Set base image (host OS)
# FROM python:3.10.12

# # Copy the content of the project directory to the working directory
# COPY . /main

# # Set the working directory in the container
# WORKDIR /main

# # Install any dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Specify the Flask environment port
# ENV PORT 5001

# # By default, listen on port 5000
# EXPOSE 5001

# # Set the directive to specify the executable that will run when the container is initiated
# ENTRYPOINT [ "python" ]

# # Specify the command to run on container start
# CMD [ "app.py" ]
# Set base image (host OS)
FROM python:alpine3.8

# Copy the content of the project directory to the working directory
COPY . /main

# Set the working directory in the container
WORKDIR /main

# Install any dependencies
RUN pip install -r requirements.txt

# Specify the Flask environment port
ENV PORT 5001

# By default, listen on port 5000
EXPOSE 5001

# Set the directive to specify the executable that will run when the container is initiated
ENTRYPOINT [ "python" ]

# Specify the command to run on container start
CMD [ "app.py" ]
