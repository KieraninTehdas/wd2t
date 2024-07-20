# frozen_string_literal: true

class Decision < ApplicationRecord
  validates :title, presence: true
end
