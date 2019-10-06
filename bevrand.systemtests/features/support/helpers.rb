require 'dotenv'

module Fixture

  def load_env
    if ENV['RUBY_ENV'] == 'Docker'
      Dotenv.load('.env.docker')
    else
      Dotenv.load('.env.local')
    end
    proxy_url = ENV['proxyapi']
    print proxy_url
    authenticationapi_url = ENV['authenticationapi']
    print authenticationapi_url
    playlistapi_url = ENV['playlistapi']
    print playlistapi_url
    FixtureData.new(proxy_url, authenticationapi_url, playlistapi_url)
  end
end

class FixtureData
  def initialize(proxy_url, authenticationapi_url, playlistapi_url)
    @proxy_url = proxy_url
    @authenticationapi_url = authenticationapi_url
    @playlistapi_url = playlistapi_url
    @token = ''
    @auth_header = 'x-api-token'
    @user = 'testusersystem'
    @email = 'testsystememail@test.nl'
    @password = 'testuserpassword'
    @proxy_login = proxy_url + '/authentication-api/login'
    @proxy_register = proxy_url + '/authentication-api/register'
    @proxy_highscore = proxy_url + '/highscore-api/v1/highscores'
    @proxy_playlist_public = proxy_url + '/playlist-api/v2/frontpage'
    @proxy_playlist_private = proxy_url + '/playlist-api/v1/private'
    @proxy_randomize = proxy_url + '/randomize-api/v2/randomize'
    @proxy_randomize_user = proxy_url + '/randomize-api/v1/randomize'
    @proxy_recommendation = proxy_url + '/recommendation-api/v1'
  end
  attr_reader :proxy_url
  attr_reader :authenticationapi_url
  attr_reader :playlistapi_url
  attr_reader :token
  attr_reader :auth_header
  attr_reader :proxy_login
  attr_reader :proxy_register
  attr_reader :proxy_highscore
  attr_reader :proxy_playlist_public
  attr_reader :proxy_playlist_private
  attr_reader :proxy_randomize
  attr_reader :proxy_randomize_user
  attr_reader :proxy_recommendation


  def clean_up_before_run
    auth_url = "#{@authenticationapi_url}/api/Users"
    response = JSON.parse(RestClient.get(auth_url, { content_type: :json, accept: :json }))
    users = response['allUsers']
    for user in users
      user_name = user['username']
      user_id = user['id'].to_i
      playlist_url_delete = "#{@playlistapi_url}/api/v1/private/#{user_name}"
      auth_url_delete = "#{auth_url}/?id=#{user_id}"
      begin
        RestClient.delete playlist_url_delete
      rescue RestClient::ExceptionWithResponse => e
        print e
      end
      begin
        RestClient.delete auth_url_delete, { content_type: :json, accept: :json }
      rescue RestClient::ExceptionWithResponse => e
        print e
      end
    end

  end
  def create_and_login_user(user, email)
    user = { 'username' => user,
             'emailAddress' => email,
             'password' => @password,
        }
    register_url = @proxy_register.to_s
    begin
      RestClient.post register_url, user.to_json, { content_type: :json, accept: :json }
    rescue RestClient::ExceptionWithResponse => e
      print e
    end

    login_url = @proxy_login.to_s
    begin
      response = RestClient.post login_url, user.to_json, { content_type: :json, accept: :json }
      json_response = JSON.parse(response)
      @token = json_response['token']
    rescue RestClient::ExceptionWithResponse => e
      print e
    end
  end

  def create_new_user
    { 'username' => self.create_random_user(15),
      'emailAddress' => self.create_random_email(),
      'password' => self.create_random_password(10)
    }
  end

  def create_random_user(length)
    [*('a'..'z'), *('A'..'Z')].sample(length).join
  end

  def create_random_email
    firstpart = [*('a'..'z'), *('A'..'Z')].sample(8).join
    secondpart = [*('a'..'z'), *('A'..'Z')].sample(8).join
    "#{firstpart}@#{secondpart}"
  end

  def create_random_password(length)
    [*('a'..'z'), *('A'..'Z'), *('0'..'9')].sample(length).join
  end

  def create_new_playlist
    {
        "displayName": "I am so depressed",
        "imageUrl": "http://whatever.com",
        "beverages": %w(beer wine coke)
    }
  end

  def create_update_playlist
    {
        "displayName": "I am no longer so depressed",
        "imageUrl": "http://whatever.nl",
        "beverages": %w(beer wine coke whiskey)
    }
  end
end

World(Fixture)