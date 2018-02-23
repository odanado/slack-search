FROM node

WORKDIR /src

ARG SLACK_CLIENT_ID
ARG SLACK_TEAM
ARG SERVER_URL

ENV SLACK_CLIENT_ID ${SLACK_CLIENT_ID}
ENV SLACK_TEAM ${SLACK_TEAM}
ENV SERVER_URL ${SERVER_URL}

ADD package.json package.json
ADD yarn.lock yarn.lock
RUN yarn
RUN node -e "console.log(process.env.SERVER_URL)"

ADD . /src
RUN yarn run build

CMD bash -c "yarn run start -H 0.0.0.0"
