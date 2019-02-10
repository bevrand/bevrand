require 'uri'
require 'json'
require 'rest-client'
require 'dotenv'

url = ''

Before do
  if ENV['RUBY_ENV'] == 'Docker'
    Dotenv.load
  else
    Dotenv.load('.env.local')
  end
  url = ENV['proxyapi']
end

Given /^we have a test environment$/ do
  response = RestClient.get("#{url}/v2/frontpage")
  expect(response.code).to be 200
end

When /^we request a random drink from the proxy$/ do
  front_page_url = "#{url}/v2/frontpage"
  response =  JSON.parse(RestClient.get(front_page_url).body)
  sut = "#{url}/v2/randomize"
  @result = RestClient.post sut, response[0].to_json, { content_type: :json, accept: :json }
end

Then /^we should get a status of '(.*)' with a random drink$/ do |code|
  expect(@result.code).to be code.to_i
end

When /^we request all playlists$/ do
  front_page_url = "#{url}/v2/frontpage"
  @json_response = RestClient.get(front_page_url).body
end

And /^we randomize from '(.*)'$/ do |playlistName|
  playlists = JSON.parse(@json_response)
  playlists.each do |playlist|
    if playlist['list'] == playlistName
      sut = "#{url}/v2/randomize"
      json = JSON.generate(playlist)
      @tgif_playlist = playlist
      @result = RestClient.post sut, json, { content_type: :json, accept: :json }
    end
  end
end

Then /^we should get a random drink from that playlist$/ do
  beverage_result = JSON.parse(@result.body)
  expect(@result.code).to be 200
  expect(@tgif_playlist['beverages']).to include(beverage_result['result'])
end

When /^I randomize from these playlists$/ do
  @results = []
  playlists = JSON.parse(@json_response)
  playlists.each do |playlist|
    sut = "#{url}/v2/randomize"
    json = JSON.generate(playlist)
    result = RestClient.post sut, json, { content_type: :json, accept: :json }
    @results.push(result.code)
  end
end

Then /^all playlists should give a result of '(.*)'$/ do |code|
  for statusCode in @results
    expect(statusCode).to be code.to_i
  end
end
