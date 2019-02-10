require 'uri'
require 'json'
require 'rest-client'
require 'dotenv'

url = ""

Before do
  if ENV['RUBY_ENV'] == 'Docker'
    Dotenv.load
  else
    Dotenv.load(".env.local")
  end
  url = ENV['proxyapi']
end

When /^we create a new user$/ do
  user = create_new_user
  sut = "#{url}/register"
  @result = RestClient.post sut, user, {content_type: :json, accept: :json}
end

Then /^we should get a result of '(.*)'$/ do |code|
  expect(@result.code).to be code.to_i
end

def create_new_user
  user = {'userName' => create_random_user(15),
          'emailAddress' => create_random_email(),
          'passWord' => create_random_password(10),
          'active' => true}
  return user
end

def create_random_user(length)
  username = [*('a'..'z'), *('A'..'Z')].to_a.shuffle[0, length].join
  return username
end

def create_random_email()
  firstpart = [*('a'..'z'), *('A'..'Z')].to_a.shuffle[0, 8].join
  secondpart = [*('a'..'z'), *('A'..'Z')].to_a.shuffle[0, 8].join
  return "#{firstpart}@#{secondpart}"
end

def create_random_password(length)
  password = [*('a'..'z'), *('A'..'Z'), *('0'..'9')].to_a.shuffle[0, length].join
  return password
end
