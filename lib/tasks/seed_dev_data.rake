namespace :db do
  task populate: [:environment] do
    require "faker"

    User.create(
      first_name: "Tony",
      last_name: "Test",
      display_name: "Big TT",
      email_address: "tony@test.test",
      password: "test"
    )
  end
end
