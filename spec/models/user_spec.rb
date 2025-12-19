require 'rails_helper'

RSpec.describe User, type: :model do
  describe "name validations" do
    let(:user) do
      User.new(
        first_name: first_name,
        last_name: last_name,
        display_name: display_name,
        email_address: "dave@test.com",
        password: "password"
      )
    end

    context "when all name fields are present" do
      let(:first_name) { "Dave" }
      let(:last_name) { "Smith" }
      let(:display_name) { "Dave Smith" }

      it "returns valid? is true" do
        expect(user.valid?).to be true
      end
    end

    context "when first_name is missing" do
      let(:first_name) { "    " }
      let(:last_name) { "Smith" }
      let(:display_name) { "Dave Smith" }

      it "returns valid? is false" do
        expect(user.valid?).to be false
      end

      it "contains an error message for first_name" do
        user.valid?

        expect(user.errors.count).to eq 1
        expect(user.errors).to include "first_name"
      end
    end

    context "when last_name is missing" do
      let(:first_name) { "Dave" }
      let(:last_name) { "" }
      let(:display_name) { "Dave Smith" }

      it "returns valid? is false" do
        expect(user.valid?).to be false
      end

      it "contains an error message for last_name" do
        user.valid?

        expect(user.errors.count).to eq 1
        expect(user.errors).to include "last_name"
      end
    end

    context "when display_name is missing" do
      let(:first_name) { "Dave" }
      let(:last_name) { "Smith" }
      let(:display_name) { "\n" }

      it "returns valid? is false" do
        expect(user.valid?).to be false
      end

      it "contains an error message for last_name" do
        user.valid?

        expect(user.errors.count).to eq 1
        expect(user.errors).to include "display_name"
      end
    end
  end
end
