import queue
import threading

from twython import TwythonStreamer


class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        if 'text' in data:
            username = data['user']['screen_name']
            tweet = data['text']
            tweet = "{}: {}".format(username, tweet)
            print(tweet)
            q.put(tweet)


    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


q = queue.Queue()


def twitter_worker():
    from local_settings import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

    stream = MyStreamer(APP_KEY, APP_SECRET,
                        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track='berlin')


def erika_worker():
    pass


# block until all tasks are done
# q.join()

#####
# TODO: shutdown
# stop workers
# for i in range(num_worker_threads):
#    q.put(None)
# for t in threads:
#    t.join()
####

def main():
    threads = []
    t = threading.Thread(target=twitter_worker)
    t.start()
    threads.append(t)

    t = threading.Thread(target=erika_worker)
    t.start()
    threads.append(t)


if __name__ == "__main__":
    main()
