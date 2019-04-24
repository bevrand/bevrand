require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
  @fixture.clean_up_before_run
end

Given /^we have randomized a few times$/ do
  front_page_url = "#{@fixture.proxy_playlist_public}"
  response =  JSON.parse(RestClient.get(front_page_url).body)
  sut = "#{@fixture.proxy_randomize}"
  response.each do |playlist|
    RestClient.post sut, playlist.to_json, { content_type: :json, accept: :json }
  end
end

When /^we randomize as (.+) for (.+)$/ do |user, playlist|
  userPlaylist = "#{@fixture.proxy_playlist_private}/#{user}/#{playlist}"
  response = JSON.parse(RestClient.get(url=userPlaylist, { content_type: :json, accept: :json, 'x-api-token' => @fixture.token }).body)
  sut = "#{@fixture.proxy_randomize}"
  5.times do
    RestClient.post sut, response[0].to_json, { content_type: :json, accept: :json }
  end
end

When /^we query the global highscore$/ do
  sut = "#{@fixture.proxy_highscore}"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end

When /^we query the (.+) and (.+) highscore$/ do |frontpage, playlist|
  sut = "#{@fixture.proxy_highscore}/#{frontpage}/#{playlist}"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end