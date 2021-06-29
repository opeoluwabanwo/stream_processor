```bash
# build the docker image for deployment
docker build -t deploy-img .

# start the container with the current folder attached as a volume
docker run -it -v $PWD:/app/ deploy-img bash

# rune the deploy script to deploy
cd app/orchestrate/shell
source deploy.sh
```
