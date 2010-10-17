# DOOod #
> somechick: have you heard about *kleenex*

> somedude: it's for your nose

> somechick: *what*?

> somedude: what what? 

You, too, can be afk while pidgin throws not-so-wittie responses at your friends.

That's what doood's for. You setup a list of "trigger phrases", and doood responds with your predefined replies.

If you think this is mostly useless, you're in the same boat as its developers. But it's fun, and we wanted to learn about DBus and pidgin, while using a programming language we're not entirely comfortable with. And one of us really wanted to write a multi-process application. We got all of that with doood. In about 12 hours. On a Saturday (it was cloudy, we were going to go on a bike ride instead).

## Configuration ##
copy and rename `example.doood_config.json` to one of three places (whichever you choose):

 * $HOME/.doood_config.json
 * $HOME/.config/.doood_config.json
 * $DOOOD_FOLDER/.doood_config.json
 
where $HOME is your home folder, and $DOOOD_FOLDER is the same folder as doood.py on your system.

Then just change the values. `users` is a list of users you want doood to respond to, and `replies` is the set of `trigger_phrase: reply` thingers.
