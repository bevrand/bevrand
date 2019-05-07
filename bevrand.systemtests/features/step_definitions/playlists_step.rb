require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
  @fixture.clean_up_before_run
end

Given /^We create (.+) with (.+)$/ do |user, email|
  @fixture.create_and_login_user(user, email)
end

When /^we create a (.+) user based (.+)$/ do |user, playlist|
  playlistToPost = @fixture.create_new_playlist
  begin
    sut = "#{@fixture.proxy_playlist_private}/#{user}/#{playlist}"
    @result = RestClient.post sut, playlistToPost.to_json, { content_type: :json, accept: :json, @fixture.auth_header => @fixture.token }
  rescue RestClient::ExceptionWithResponse => e
    @result = e.response
  end
end

When /^we update a (.+) user based (.+)$/ do |user, playlist|
  playlistToUpdate = @fixture.create_update_playlist
  begin
    sut = "#{@fixture.proxy_playlist_private}/#{user}/#{playlist}"
    @result = RestClient.put sut, playlistToUpdate.to_json, { content_type: :json, accept: :json, @fixture.auth_header => @fixture.token }
  rescue RestClient::ExceptionWithResponse => e
    @result = e.response
  end
end

When /^we delete all playlists for (.+)$/ do |user|
  sut = "#{@fixture.proxy_playlist_private}/#{user}"
  begin
    @result = RestClient.delete sut, { content_type: :json, accept: :json, @fixture.auth_header => @fixture.token }
  rescue RestClient::ExceptionWithResponse => e
    @result = e.response
  end
end

Then /^we should be able to retrieve (.+) playlists$/ do |user|
  sut = "#{@fixture.proxy_playlist_private}/#{user}"
  @json_response = RestClient.get(sut, { content_type: :json, accept: :json, @fixture.auth_header => @fixture.token }).body
end

Then /^the number of returned playlists should be (.+)$/ do |numberoflists|
  expect(JSON.parse(@json_response)['result'].length).to eq numberoflists.to_i
end

Then /^the (.+) should be updated to (.+)$/ do |field, updated|
  expect(JSON.parse(@json_response)['result'][0][field]).to eq updated
end

Then /^we should get a result of (.+)$/ do |code|
  expect(@result.code).to be code.to_i
end
