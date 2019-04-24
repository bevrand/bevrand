require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
  @fixture.clean_up_before_run
end

When /^we create a new user$/ do
  user = @fixture.create_new_user
  sut = (@fixture.proxy_register).to_s
  @result = RestClient.post sut, user.to_json, { content_type: :json, accept: :json }
end

Then(/^we should get a result of (\d+)$/) do |code|
  expect(@result.code).to be code.to_i
end