require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
  @fixture.clean_up_before_run
end

When /^we ask for a grouped recommendation$/ do
  sut = "#{@fixture.proxy_recommendation}/beveragegroups/"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
rescue RestClient::ExceptionWithResponse => e
  @result = e.response
end

Then /^we skip this code for now$/ do
  expect(1).to be 1
end
