# Python module to submit listens to the ListenBrainz service

Simple python module to submit listens to the ListenBrainz server.

Supports submitting single listens, now playing notifications and import of
multiple listens. Automatically honors the ListenBrainz server's rate limits.


## Usage

```python
import time
from listenbrainz_submit import ListenBrainzClient, Track


# The user's personal ListenBrainz token obtained from https://listenbrainz.org/profile/
user_token = "..."
client = ListenBrainzClient(user_token=user_token)

# Prepare a track to submit
track = Track(
    artist_name="Dool",
    track_name="Vantablack",
    release_name="Here Now, There Then",
    additional_info={
        "listening_from": "My great music player",
        "recording_mbid": "e225fb84-dc9a-419e-adcd-9890f59ec432",
        "release_mbid": "aa1ea1ac-7ec4-4542-a494-105afbfe547d",
        "artist_mbids": "24412926-c7bd-48e8-afad-8a285b42e131",
        "tracknumber": 1,
    }
)

# Inform ListenBrainz that this track is playing right now. ListenBrainz
# will display this track on the user's listens page as being currently played.
client.playing_now(track)
```

To actually submit a track as has been listened to call:

```python
# Submit the listen with a current timestamp
client.listen(int(time.time()), track)
```

For details on the API usage please refer to the
[ListenBrainz API documentation](https://listenbrainz.readthedocs.io/en/production/),
especially the [Payload JSON details](https://listenbrainz.readthedocs.io/en/production/dev/json/#payload-json-details)
which describes the metadata that can be submitted.


# License

listenbrainz-submit © 2018-2022 Philipp Wolfer ph.wolfer@gmail.com

Published under the MIT license, see LICENSE for details.
