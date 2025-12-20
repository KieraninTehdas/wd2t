class User < ApplicationRecord
  has_secure_password
  has_many :sessions, dependent: :destroy
  has_many :decisions, inverse_of: :creator, dependent: :destroy

  validates :first_name, :last_name, :display_name, presence: true

  normalizes :email_address, with: ->(e) { e.strip.downcase }
end
