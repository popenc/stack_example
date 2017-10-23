# Example of the technology stack used for CTS:

	nodejs, socket.io, celery, django, redis

# Run with docker:

	$ cd ./stack_example
	$ docker-compose up

Should be able to access page at: http://localhost/app/testing

When I'm on my windows machine, I have to use the docker-machine IP:

(for me): http://192.168.99.100/app/testing


# About:
When the "Send message" button is clicked, the frontend sends a message to nodejs via socket.io.
Then, that message is passed to the celery worker, which sends a message back to nodejs saying
that it received the message. This message then gets pushed from nodejs back to the user, which is
seen as an alert popup saying "hello from celery."





TODO: Add logging on page instead of in docker logs and console logs, so it's
easier to follow what's going on.
TODO: Although the current sctructure is like QED, I think it'd be cleaner, for the example, to have all django related everything inside a "django project" folder to help show the separation of the different stack elements.
