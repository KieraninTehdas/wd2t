require 'rails_helper'

RSpec.describe "SignUps", type: :request do
  describe "GET /show" do
    it "returns http success" do
      get "/sign_ups/show"
      expect(response).to have_http_status(:success)
    end
  end

end
