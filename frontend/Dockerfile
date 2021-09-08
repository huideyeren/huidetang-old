FROM node:14-bullseye-slim
WORKDIR /opt/next

COPY ./components ./components
COPY ./interfaces ./interfaces
COPY ./pages ./pages
COPY ./public ./public
COPY ./utils ./utils
COPY ./.babelrc ./.babelrc
COPY ./.editorconfig ./.editorconfig
COPY ./.eslintrc.js ./.eslintrc.js
COPY ./.prettierignore ./.prettierignore
COPY ./jest.congig.js ./jest.congig.js
COPY ./next-env.d.ts ./next-env.d.ts
COPY ./package.json ./package.json
COPY ./yarn.lock ./yarn.lock
COPY ./tsconfig.json ./tsconfig.json

RUN yarn install --frozen-lockfile && yarn build && \
    groupadd -r next && useradd -r -g next next && chown -R next:next .next

USER next
CMD ["yarn", "start"]
