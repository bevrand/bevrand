require 'uri'
require 'json'
require 'rest-client'
require 'dotenv'

Before do
  @fixture = load_env
end

When /^we ask for a grouped recommendation$/ do
  sut = "#{@fixture.url}/recommendation-api/v1/beveragegroups/"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end