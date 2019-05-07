require 'uri'
require 'json'
require 'rest-client'

Before do
  @fixture = load_env
  @fixture.clean_up_before_run
end

Given /^we have randomized a few times$/ do
  front_page_url = (@fixture.proxy_playlist_public).to_s
  response =  JSON.parse(RestClient.get(front_page_url).body)
  sut = (@fixture.proxy_randomize).to_s
  response.each do | playlist |
    3.times do
      RestClient.post sut, playlist.to_json, { content_type: :json, accept: :json }
    end
  end
end

When /^we randomize as (.+) for (.+)$/ do |user, playlist|
  userPlaylist = "#{@fixture.proxy_playlist_private}/#{user}/#{playlist}"
  response = JSON.parse(RestClient.get(url=userPlaylist, { content_type: :json, accept: :json, @fixture.auth_header => @fixture.token }).body)
  sut = (@fixture.proxy_randomize_user).to_s
  body_to_post = response['result']
  @results = []
  5.times do
    result = RestClient.post sut, body_to_post.to_json, { content_type: :json, accept: :json, @fixture.auth_header => @fixture.token}
    @results.push(result.code)
  end
end

When /^we query the global highscore$/ do
  sut = (@fixture.proxy_highscore + '/').to_s
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end

When /^we query the (.+) and (.+) highscore$/ do |frontpage, playlist|
  sut = "#{@fixture.proxy_highscore}/#{frontpage}/#{playlist}"
  @result = RestClient.get sut, { content_type: :json, accept: :json }
end