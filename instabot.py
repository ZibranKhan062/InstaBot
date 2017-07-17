#https://acadview.com/student/dashboard#access_token=5699864983.81e0027.1002e9a68f6c456e8f4eac525870d9d1

import requests
import urllib
from termcolor import colored
from textblob import TextBlob

print colored ('\n\t\t\t\t\t[Sandboxed Users are: test_account786 ]\n','red',attrs=['bold'])

username='test_account786'

#Function for proper authentication,only owner and Sandbox Users can access it

def authentication():
    i = True
    while i:
        insta_username = raw_input('Enter Sandboxed UserName:')
        if len(insta_username) == 0:
            print'Please enter a valid name:'

        elif insta_username != 'test_account786':
                print'Not a Sandboxed User!,please enter a Valid Sandboxed Username'

        else:
            print'\nAuthentication Granted :)'
            break
authentication()

APP_ACCESS_TOKEN = '5699864983.4a78ce6.2a837d990d804bc485358abfac85aad1'        #Global Variable for App Access Token
BASE_URL = 'https://api.instagram.com/v1/'                                      #Global Variable for Base URL

#-------------Function Declaration for getting Self Information--------------------

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url :%s \n' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Your Username is: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts till now: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


#------------Function Declaration for getting User Identity (User ID)-----------------
#insta_username='zibrankhan9060'
def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          return user_info['data'][0]['id']

      else:
          return None
  else:
      print 'Status code other than 200 received!'
      exit()

#-----------Function Declaration for getting User Information------------

def get_user_info(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code'] == 200:
      if len(user_info['data']):
          print '\nUsername: %s' % (user_info['data']['username'])
          print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
          print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
          print 'No. of posts till now: %s' % (user_info['data']['counts']['media'])
      else:
          print 'There is no data for this user!'
  else:
      print 'Status code other than 200 received!'

#---------Function Declaration for getting own Shared Recent Post--------------

def get_own_post():
  request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
  print'  \n ---> Please hold on,showing your most recent post'
  print 'GET request url : %s' % (request_url)

  own_media = requests.get(request_url).json()
  if own_media['meta']['code'] == 200:
      if len(own_media['data']):
          image_name = own_media['data'][0]['id'] + '.jpeg'
          image_url = own_media['data'][0]['images']['standard_resolution']['url']
          urllib.urlretrieve(image_url, image_name)
          print 'Your image has been downloaded! \n\tand now will open in your browser'
          print'Done!'
          import webbrowser
          webbrowser.open(image_url)
          return own_media['data'][0]['id']
      else:
          print 'Post does not exist!'
  else:
      print 'Status code other than 200 received!'
  return None

#---------Function Declaration for getting sandbox user recent post------------

def get_user_post(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  print'Hold On.. Showing recent post of %s:' % (username)
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)

  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()
  if user_media['meta']['code'] == 200:
      if len(user_media['data']):
          image_name = user_media['data'][0]['id'] + '.jpeg'
          image_url = user_media['data'][0]['images']['standard_resolution']['url']
          urllib.urlretrieve(image_url, image_name)
          print '\nYour image has been downloaded! \n\t and now will open in your browser\n'
          import webbrowser
          webbrowser.open(image_url)
          return user_media['data'][0]['id']
      else:
          print "There is no recent post!"
  else:
      print "Status code other than 200 received!"
  return None


#------------Function Declaration for getting Post ID------------

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    #print'This is get post ID'
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

#---------Function Declaration for Liking a post-------------

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print '\nLike was successful!'
    else:
        print '\n\tYour like was unsuccessful. Try again!'

#---------Function Declaration for posting a comment--------------

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Enter your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print colored("\n Done!!\n\tSuccessfully added a new comment!",attrs=['bold'])
    else:
        print "Unable to add comment. Try again!"

#--------Function Declaration for showing comments on a post----------------

def list_comments(insta_username):
    user_id = get_post_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL +'media/%s/comments?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url :%s ' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print'\n--> Comments are:\n'
            id=1
            for temp in user_info['data']:
                print'%s. %s' % (id,temp['text'])
                id+=1
            print'------------------------------------'
        else:
            print 'no comments'
    else:
        print 'Status code other than 200 received!'

#--------Function Declaration for setting latitude and Longitude--------

def set_location(latitude,longitude):
    request_url=(BASE_URL + 'locations/search?lat=%s&lng=%s&access_token=%s') %(latitude,longitude,APP_ACCESS_TOKEN)
    print 'GET request url: %s' %(request_url)
    user_location=requests.get(request_url).json()
    print user_location
    if user_location['meta']['code']==200:
        if len(user_location['data']):
            return user_location['data'][0]['id']

        else:
            print 'No location existed'
            return None
    else:
        print 'Status code other than 200 received'
        exit()

#------Function Declaration for receiving tags from User-----------

def receive_tags(tag_name):
    request_url = (BASE_URL + 'tags/search?q=%s&access_token=%s') % (tag_name, APP_ACCESS_TOKEN)
    print 'GET request url: %s' % (request_url)
    related_tag = requests.get(request_url).json()
    print related_tag
    if related_tag['meta']['code']==200:
        if len(related_tag['data']):
            return related_tag['data']
        else:
            print'No tags available at Instagram Database'
            return None
    else:
        print 'Status code other than 200  received'
        exit()

#----------Function Declaration for getting tagged media----------

def get_tag_media(tag_name):
    if tag_name==None:
        print "No image exist"
        exit()
    request_url = (BASE_URL + 'tags/%s/media/recent?access_token=%s') % (tag_name,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    tag_media = requests.get(request_url).json()

    if tag_media['meta']['code']==200:
        if len(tag_media['data']):
            image_name = tag_media['data'][0]['id'] + '.jpeg'
            print image_name
            image_url = tag_media['data'][0]['images']['standard_resolution']['url']
            print image_url
            urllib.urlretrieve(image_url, image_name)
            print 'Your post has been downloaded'
            import webb
            rowser
            webbrowser.open(image_name)
            return tag_media['data'][0]['id']
        else:
            print "No such post exist"
            return None
    else:
        print 'Status code other than 200 received'


print colored('\n\t\t\t\----------- Welcome to InstaBot -------------/','magenta',attrs=['bold','concealed'])
def menu():
    i = True
    while i:

        print colored('  MENU:',attrs=['bold'])
        print colored('\n1. Know ur own info','red',attrs=['bold'])
        print colored('2. Get user ID','red',attrs=['bold'])
        print colored('3. Get User Info','red',attrs=['bold'])
        print colored('4. Show your own recent Post','red',attrs=['bold'])
        print colored('5. Get recent liked post of Sandboxed User','red',attrs=['bold'])
        print colored('6. Get post ID','red',attrs=['bold'])
        print colored('7. Like a post of Sandboxed User(recent one)','red',attrs=['bold'])
        print colored('8. Post a comment','red',attrs=['bold'])
        print colored('9. Get list of comments','red',attrs=['bold'])
        print colored('10.Get Location','red',attrs=['bold'])
        print colored('11.Exit','red',attrs=['bold'])

        choice = int(raw_input ('\tEnter your Choice:'))

        if choice == 1:
            self_info()

        elif choice == 2:
            get_user_id(username)
            b = get_user_id(username)
            print '\nID for %s is:' % (username), b

        elif choice == 3:
            get_user_info(username)


        elif choice==4:
            get_own_post()

        elif choice==5:
            get_user_post(username)

        elif choice==6:
            print'Fetching ID of Post of user %s' %(username)
            get_post_id(username)
            z=get_post_id(username)
            print 'Post ID is',z

        elif choice==7:
            like_a_post(username)

        elif choice==8:
            post_a_comment(username)

        elif choice==9:
            list_comments(username)



        elif choice == 10:
            latitude = float(raw_input("Enter latitude:"))
            longitude = float(raw_input("Enter longitude"))
            set_location(latitude, longitude)
            print 'Available tags are'
            print '\t1.Earthquake\n\t2.Flood\n\t3.Landslide'
            tag_name = raw_input("Enter name of tag")
            if tag_name == 'Earthquake' or tag_name == '1':
                receive_tags(tag_name)
                get_tag_media(tag_name)
            elif tag_name == 'Flood' or tag_name == '2':
                receive_tags(tag_name)
                get_tag_media(tag_name)
            elif tag_name == 'landslide' or tag_name == '3':
                receive_tags(tag_name)
                get_tag_media(tag_name)
            else:
                print 'Wrong input,please enter a valid option'


        elif choice == 11:
            print colored('\n----Thanks For using my InstaBot-----\n\t:) Have a Good Day :)','magenta',attrs=['bold'])
            exit()
        else:
            print'\tInavlid Input! please enter between(1-10)'
menu()







