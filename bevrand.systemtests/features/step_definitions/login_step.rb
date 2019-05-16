When /^we login this created user using (.+)$/ do |field|
  begin
    user = { field => @random_user[field],
             'password' => @random_user['password']
    }
    @login_result = RestClient.post @fixture.proxy_login, user.to_json, { content_type: :json, accept: :json }
  rescue RestClient::ExceptionWithResponse => e
    @login_result = e.response
  end
end

Then /^the result has (.+) and a token attached$/ do |code|
  expect(@login_result.code).to be code.to_i
  parsedResult = JSON.parse(@login_result)
  expect(parsedResult['success']).to be true
  expect(parsedResult['token']).not_to be_empty
end

