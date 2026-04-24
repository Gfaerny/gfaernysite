#!/usr/bin/env bash

find . -type f -name 'index.html' | while IFS= read -r file
do
    if ! sed -n '1p' "$file" | grep -q '<!-- Added automaticly -->'; then
        sed -i '1i\
<!-- Added automaticly -->\
<!DOCTYPE html>\
<html lang="en">\
\
  <head>\
    <meta charset="utf-8" />\
    <meta name="viewport" content="width=device-width,initial-scale=1" />\
    <link rel="stylesheet" href="css/styles.css">\
  <title>gfaerny</title>\
    </head>\
\
\
    <body>\
      <div class="container">\
        <header>\
          <h1><a href="https://gfaerny.me">gfaerny</a></h1>\
          <p class="meta">\
\
            Email:\
            <a href="mailto:mail@gfaerny.me">mail@gfaerny.me</a><br>\
            <a href="https://github.com/gfaerny/">Github</a> —\
            <a href="https://gfaerny.bandcamp.com">Bandcamp</a> —\
            <a href="https://soundcloud.com/gfaerny">Soundcloud</a> —\
            <a rel="me" href="https://mastodon.art/@gfaerny">Mastodon</a>\
\
          </p>\
        </header>\
<!-- Added automaticly -->\
' "$file"
    fi
done
