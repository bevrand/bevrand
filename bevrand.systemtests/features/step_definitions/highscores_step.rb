require 'uri'
require 'json'
require 'rest-client'
require 'dotenv'

Before do
  @fixture = load_env
end

When /^we ask for the global highscore$/ do
  sut = "#{@fixture.url}/highscore-api/v1/highscores/"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end