require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
end

Given /^we have randomized a few times$/ do
  front_page_url = "#{@fixture.url}/playlist-api/v2/frontpage"
  response =  JSON.parse(RestClient.get(front_page_url).body)
  sut = "#{@fixture.url}/randomize-api/v2/randomize"
  response.each do |playlist|
    RestClient.post sut, playlist.to_json, { content_type: :json, accept: :json }
  end
end

When /^we randomize as (.+) for (.+)$/ do |user, playlist|
  userPlaylist = "#{@fixture.url}/playlist-api/api/v1/private/#{user}/#{playlist}"
  response = JSON.parse(RestClient.get(url=userPlaylist, { content_type: :json, accept: :json, 'x-api-token' => 'Bearer ' + @fixture.token }).body)
  sut = "#{@fixture.url}/randomize-api/v2/randomize"
  5.times do
    RestClient.post sut, response[0].to_json, { content_type: :json, accept: :json }
  end
end

When /^we query the global highscore$/ do
  sut = "#{@fixture.url}/highscore-api/v1/highscores/"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end

When /^we query the (.+) and (.+) highscore$/ do |frontpage, playlist|
  sut = "#{@fixture.url}/highscore-api/v1/highscores/#{frontpage}/#{playlist}"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end