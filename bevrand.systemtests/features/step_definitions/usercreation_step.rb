require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
  @fixture.clean_up_before_run
end

When /^we create a new user$/ do
  user = @fixture.create_new_user
  @random_user = user
  sut = (@fixture.proxy_register).to_s
  @result = RestClient.post sut, user.to_json, { content_type: :json, accept: :json }
end
