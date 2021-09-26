.PHONY: clean server

VERSION=0.1
all: clean server 
	docker images -f dangling=true -q | xargs docker rmi -f 

server:
	docker build -t altonomy .

clean:
	docker images --filter=reference='altonomy*' -q | xargs docker rmi -f || true