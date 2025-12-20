require 'rails_helper'

RSpec.feature "SignUps", type: :feature do
  scenario "User signs up for an account" do
    visit "/"

    click_link "Create one"

    fill_in "First name", with: "Jane"
    fill_in "Last name", with: "Smith"
    fill_in "Email address", with: "jane.smith@test.dev"
    fill_in "Password", with: "very secret"
    fill_in "Password confirmation", with: "very secret"

    click_button "Sign up"

    expect(page).to have_content "Why Did We Do That?"
    expect(page).to have_content "+ Decision"
    expect(page).to have_current_path "/"
  end
end
