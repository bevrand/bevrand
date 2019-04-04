module Fixture

  def load_env
    if ENV['RUBY_ENV'] == 'Docker'
      Dotenv.load('.env.docker')
    else
      Dotenv.load('.env.local')
    end
    url = ENV['proxyapi']
    FixtureData.new(url)
  end
end

class FixtureData
  def initialize(url)
    @url = url
  end
  attr_reader :url

  def create_new_user
    { 'username' => @fixture.create_random_user(15),
      'emailAddress' => @fixture.create_random_email(),
      'password' => @fixture.create_random_password(10)
    }
  end

  def create_random_user(length)
    [*('a'..'z'), *('A'..'Z')].sample(length).join
  end

  def create_random_email
    firstpart = [*('a'..'z'), *('A'..'Z')].sample(8).join
    secondpart = [*('a'..'z'), *('A'..'Z')].sample(8).join
    "#{firstpart}@#{secondpart}"
  end

  def create_random_password(length)
    [*('a'..'z'), *('A'..'Z'), *('0'..'9')].sample(length).join
  end

end

World(Fixture)