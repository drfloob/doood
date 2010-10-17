# DOOod #
> somechick: have you heard about *kleenex*

> somedude: it's for your nose

> somechick: *what*?

> somedude: what what? 

You, too, can be afk while pidgin throws not-so-wittie responses at your friends.

That's what doood's for. Doood acts as a plugin for pidgin, communicating via DBus. You get to setup your list of "trigger phrases", and doood responds with your predefined replies.

If you think this is mostly useless, you're in the same boat as its developers. But it's fun, and we wanted to learn about DBus and pidgin, while using a programming language we're not entirely comfortable with. And one of us really wanted to write a multi-process application. We got all of that with doood. In about 12 hours. On a Saturday (it was cloudy; we were going to go on a bike ride instead).

## Configuration ##
copy and rename `example.doood_config.json` to one of three places (whichever location you choose; if you have more than one, the first one found wins):

 * $DOOOD_FOLDER/.doood_config.json
 * $HOME/.config/.doood_config.json
 * $HOME/.doood_config.json
 
where $HOME is your home folder, and $DOOOD_FOLDER is the same folder where you'll find doood.py on your system.

`users` is a list of users you want doood to respond to, and `replies` is the set of `trigger_phrase: reply` thingers.

## Running DOOod ##

Execute `doood.py --parallel`. Other flags include `-v` for verbose, and `-d` for debug (more verbose). If you run it without the `--parallel` flag, you'll see why it needs to be parallelized (Hint: try having multiple people all trigger a response at the same time).

## License ##

BSD LICENSE, baby!!!

Copyright (c) 2010, crappile and drfloob

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
 * The names of its contributors may not be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.