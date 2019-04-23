require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
end

Given /^(.+) with (.+) does not exist$/ do |user, email|
  @fixture.create_and_login_user(user, email)
  sut = "#{@fixture.url}/playlist-api/api/v1/private/#{user}"
  begin
    RestClient.delete sut, { content_type: :json, accept: :json, :'x-api-token' => 'Bearer ' + @fixture.token }
  rescue RestClient::ExceptionWithResponse => e
    puts e.response
  end
end

When /^we create a (.+) user based (.+)$/ do |user, playlist|
  playlistToPost = @fixture.create_new_playlist
  begin
    sut = "#{@fixture.url}/playlist-api/api/v1/private/#{user}/#{playlist}"
    @result = RestClient.post sut, playlistToPost.to_json, { content_type: :json, accept: :json, 'x-api-token' => 'Bearer ' + @fixture.token }
  rescue RestClient::ExceptionWithResponse => e
    @result = e.response
  end
end

When /^we delete all playlists for (.+)$/ do |user|
  sut = "#{@fixture.url}/playlist-api/api/v1/private/#{user}"
  begin
    @result = RestClient.delete sut, { content_type: :json, accept: :json, 'x-api-token' => 'Bearer ' + @fixture.token  }
  rescue RestClient::ExceptionWithResponse => e
    @result = e.response
  end
end

Then /^we should be able to retrieve (.+) playlists$/ do |user|
  sut = "#{@fixture.url}/playlist-api/api/v1/private/#{user}"
  @json_response = RestClient.get(sut, { content_type: :json, accept: :json, 'x-api-token' => 'Bearer ' + @fixture.token }).body
end

Then /^the number of returned playlists should be (.+)$/ do |numberoflists|
  puts @json_response
end

