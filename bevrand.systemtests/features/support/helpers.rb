require 'dotenv'

module Fixture

  def load_env
    if ENV['RUBY_ENV'] == 'Docker'
      Dotenv.load('.env.docker')
    else
      Dotenv.load('.env.local')
    end
    url = ENV['proxyapi']
    FixtureData.new(url)
  end
end

class FixtureData
  def initialize(url)
    @url = url
    @token = ''
    @user = "testusersystem"
    @email = "testsystememail@test.nl"
    @password = "testuserpassword"
  end
  attr_reader :url
  attr_reader :token

  def create_and_login_user(user, email)
    user = { 'username' => user,
             'emailAddress' => email,
             'password' => @password,
        }
    register_url = "#{@url}/authentication-api/register"
    begin
      RestClient.post register_url, user.to_json, { content_type: :json, accept: :json }
    rescue RestClient::ExceptionWithResponse => e
      puts e.response
    end

    login_url = "#{@url}/authentication-api/login"
    begin
      response = RestClient.post login_url, user.to_json, { content_type: :json, accept: :json }
      json_response = JSON.parse(response)
      @token = json_response['token']
      print @token
    rescue RestClient::ExceptionWithResponse => e
      puts e.response
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

end

World(Fixture)