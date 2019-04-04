require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
end

When /^we create a new user$/ do
  user = @fixture.create_new_user
  sut = "#{@fixture.url}/authentication-api/register"
  @result = RestClient.post sut, user.to_json, { content_type: :json, accept: :json }
end

Then /^we should get a result of (.+)$/ do |code|
  expect(@result.code).to be code.to_i
end