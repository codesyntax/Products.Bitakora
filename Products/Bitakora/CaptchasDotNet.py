#
# Pyhton module for easy utilization of the free captchas.net CAPTCHA service
#
# For documentation look at http://captchas.net/sample/python/
#
# Written by Sebastian Wilhelmi <seppi@seppi.de>.
# This file is in the public domain.
#
# ChangeLog:
#
# 2006-03-01: Only delete the random string from the repository in
#             case of a successful verification.
#
# 2006-02-14: Add new image() method returning an HTML/JavaScript
#             snippet providing a fault tolerant service.
#
# 2005-06-02: Initial version.
#

import os
import md5
import random
import time


class CaptchasDotNet:
    def __init__ (self, client, secret,
                  random_repository= '/tmp/captchasnet-random-strings',
                  cleanup_time = 3600):
        self.__client = client
        self.__secret = secret
        self.__random_repository = random_repository
        self.__cleanup_time = cleanup_time
        self.__time_stamp_file = os.path.join(random_repository,
                                              '__time_stamp__')

    # Return a random string
    def __random_string(self):
        # The random string shall consist of small letters, big letters
        # and digits.
        letters = "abcdefghijklmnopqrstuvwxyz"
        letters += letters.upper() + "0123456789"

        # The random starts out empty, then 40 random possible characters
        # are appended.
        random_string = ''
        for i in range(40):
            random_string += random.choice(letters)

        # Return the random string.
        return random_string

    # Create a new random string and register it.
    def random(self):
        # If the repository directory is does not yet exist, create it.
        if not os.path.isdir(self.__random_repository):
            os.makedirs(self.__random_repository)

        # If the time stamp file does not yet exist, create it.
        if not os.path.isfile(self.__time_stamp_file):
            os.close(os.open(self.__time_stamp_file, os.O_CREAT, 0700))

        # Get the current time.
        now = time.time()

        # Determine the time, before which to remove random strings.
        cleanup_time = now - self.__cleanup_time

        # If the last cleanup is older than specified, cleanup the
        # directory.
        if os.stat(self.__time_stamp_file).st_mtime < cleanup_time:
            os.utime(self.__time_stamp_file, (now, now))
            for file_name in os.listdir(self.__random_repository):
                file_name = os.path.join(self.__random_repository, file_name)
                if os.stat(file_name).st_mtime < cleanup_time:
                    os.unlink(file_name)

        # loop until a valid random string has been found and registered.
        while True:
            # generate a new random string.
            random = self.__random_string()

            # open a file with the corresponding name in the repository
            # directory in such a way, that the creation fails, when the
            # file already exists. That should be near to impossible with
            # good seeding of the random number generator, but it's better
            # to play safe.
            try:
                os.close(os.open(os.path.join(self.__random_repository,
                                                 random),
                                   os.O_EXCL | os.O_CREAT, 0700))
            except EnvironmentError, error:
                # if the file already existed, rerun the loop to try the
                # next string.
                if errno.errno == errno.EEXIST:
                    continue
                else:
                    # other errors will certainly persist for other random
                    # strings, so raise the exception.
                    raise

            # return the successfully registered random string.
            self.__random = random
            return random

    def url(self, random=None, base='http://image.captchas.net/'):
        if not random:
            random = self.__random
        return '%s?client=%s&amp;random=%s' % (base, self.__client, random)

    def image(self, random=None, id='captchas.net',
               width=240, height=80):
        return '''
        <a href="http://captchas.net"><img
            style="border: none; vertical-align: bottom"
            id="%s" src="%s" width="%d" height="%d"
            alt="The CAPTCHA image" /></a>
        <script type="text/javascript">
          <!--
          function captchas_image_error (image)
          {
            if (!image.timeout) return true;
            image.src = image.src.replace (/^http:\/\/image\.captchas\.net/,
                                           'http://image.backup.captchas.net');
            return captchas_image_loaded (image);
          }

          function captchas_image_loaded (image)
          {
            if (!image.timeout) return true;
            window.clearTimeout (image.timeout);
            image.timeout = false;
            return true;
          }

          var image = document.getElementById ('%s');
          image.onerror = function() {return captchas_image_error (image);};
          image.onload = function() {return captchas_image_loaded (image);};
          image.timeout
            = window.setTimeout(
               "captchas_image_error (document.getElementById ('%s'))",
               10000);
          image.src = image.src;
          //-->
        </script>''' % (id, self.url(random), width, height, id, id)

    def validate(self, random):
        self.__random = random

        file_name = os.path.join(self.__random_repository, random)

        # Find out, whether the file exists
        result = os.path.isfile(file_name)

        # if the file exists, remember it.
        if result:
            self.__random_file = file_name

        # the random string was valid, if and only if the
        # corresponding file existed.
        return result

    def verify(self, input, random=None):
        if not random:
            random = self.__random

        # The format of the password.
        password_letters = "abcdefghijklmnopqrstuvwxyz"
        password_length = 6

        # If the user input has the wrong lenght, it can't be correct.
        if len(input) != password_length:
            return False

        # Calculate the MD5 digest of the concatenation of secret key and
        # random string.
        digest = md5.new(self.__secret + random).digest()

        # Check the password according to the rules from the first 6
        # positions of the digest.
        for pos in range(password_length):
            letter_num = ord(digest[pos]) % len(password_letters)
            # If the letter at the current position is wrong, the user
            # input isn't correct.
            if input[pos] != password_letters[letter_num]:
                return False

        # Remove the correspondig random file, if it exists.
        try:
            os.unlink(self.__random_file)
            del self.__random_file
        except:
            pass

        # The user input was correct.
        return True
